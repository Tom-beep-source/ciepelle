# Montage des pubs « UGC » (style téléphone, sous-titres TikTok) à partir des plans Kling réalistes.
# Usage : python3 ugc.py A|B|C   -> sortie/ciepelle-ugc-X.mp4
# Plans attendus dans clips/ : K1.mp4 (selfie miroir), K2.mp4 (étirement), K3.mp4 (polaire),
# K5.mp4 (rue en hiver), K4.png (avant : collant noir opaque)
import sys, os, math, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, 'clips')
SANS = os.path.join(HERE, '..', 'kling-variantes', 'assets', 'Manrope.ttf')
SERIF = os.path.join(HERE, '..', 'kling-variantes', 'assets', 'DMSerifDisplay-Regular.ttf')
ROSE = (181, 84, 111); INK = (34, 27, 31); CREAM = (251, 246, 242)

V = sys.argv[1]
OFFER = '2 pary za 149 zł'
OFFER2 = '220 g · darmowa dostawa · 14 dni na zwrot'
# (plan, début dans le plan en s, durée en s, vitesse, sous-titre)
ADS = {
 # A – « Z tego… na to » (structure Woolisi, 188 000 personnes en 2 semaines)
 'A': [('K4', 0.0, 1.3, 1.0, 'Z tego…'),
       ('K1', 0.2, 2.4, 1.0, '…na to'),
       ('K3', 0.3, 2.8, 1.0, 'A w środku|ciepły polar'),
       ('P1', 0.0, 1.4, 1.0, 'Z zewnątrz wyglądają|jak cienkie rajstopy'),
       ('V1', 2.98, 1.2, 1.0, '#Cielisty'),
       ('V2', 0.23, 1.2, 1.0, '#Czarny'),
       ('V3', 0.27, 1.2, 1.0, '#Szary'),
       ('O4', 0.8, 2.6, 1.0, None)],
 # B – « To nie są gołe nogi » (structure Ufali / Greedass : on croit à des jambes nues, preuve)
 'B': [('K1', 1.0, 2.2, 1.0, 'To nie są|gołe nogi…'),
       ('P1', 0.0, 1.5, 1.0, '…to rajstopy|z polarem'),
       ('K3', 0.3, 2.8, 1.0, 'Zobacz, co mają|w środku'),
       ('O1', 0.5, 1.1, 1.15, 'Sukienki i spódnice|nawet zimą'),
       ('O3', 0.8, 1.1, 1.15, 'Sukienki i spódnice|nawet zimą'),
       ('O5', 0.67, 1.1, 1.15, 'Sukienki i spódnice|nawet zimą'),
       ('VS', 2.4, 2.8, 1.0, None)],
 # C – marché polonais (Dessove / Ricca : « wyglądają jak prześwitujące, a w środku polar »)
 'C': [('VS', 2.4, 2.6, 1.0, 'Zimno, a ona|w cienkich rajstopach?'),
       ('K3', 0.3, 2.8, 1.0, 'Sekret?|Polar w środku'),
       ('K1', 0.0, 2.2, 1.0, 'Z zewnątrz wyglądają|jak gołe nogi'),
       ('V1', 2.98, 1.1, 1.0, '#Cielisty'),
       ('V2', 0.23, 1.1, 1.0, '#Czarny'),
       ('V3', 0.27, 1.1, 1.0, '#Szary'),
       ('O1', 0.5, 2.6, 1.0, None)],
}
SEGS = ADS[V]
END = 2.4  # le dernier plan porte l'offre

def font(s, w=800):
    f = ImageFont.truetype(SANS, s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f

def tiktok_text(lines, size=66):
    """Texte blanc gras à contour noir, comme les sous-titres natifs TikTok/Reels."""
    f = font(size); d0 = ImageDraw.Draw(Image.new('L', (1, 1)))
    ws = [d0.textlength(l, font=f) for l in lines]; lh = int(size * 1.22)
    im = Image.new('RGBA', (int(max(ws)) + 40, lh * len(lines) + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (l, w) in enumerate(zip(lines, ws)):
        d.text(((im.width - w) / 2, 12 + i * lh), l, font=f, fill=(255, 255, 255, 255), stroke_width=7, stroke_fill=(0, 0, 0, 255))
    return im

def pill(text, size, bg, fg):
    f = font(size); d0 = ImageDraw.Draw(Image.new('L', (1, 1))); w = d0.textlength(text, font=f)
    px, py = 34, 20; im = Image.new('RGBA', (int(w + 2 * px), int(size * 1.15 + 2 * py)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=im.height // 2, fill=bg)
    d.text((px, py - size * 0.08), text, font=f, fill=fg); return im

def badge():
    f = ImageFont.truetype(SERIF, 44); d0 = ImageDraw.Draw(Image.new('L', (1, 1))); w = d0.textlength('Ciepelle', font=f)
    im = Image.new('RGBA', (int(w + 52), 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, 69], radius=35, fill=INK + (190,)); d.text((26, 8), 'Ciepelle', font=f, fill=CREAM)
    return im
BADGE = badge()

class Src:
    def __init__(s, name):
        p = os.path.join(C, name)
        if os.path.exists(p + '.png') or os.path.exists(p + '.jpg'):
            f = cv2.cvtColor(cv2.imread(p + ('.png' if os.path.exists(p + '.png') else '.jpg')), cv2.COLOR_BGR2RGB)
            s.still = cover(f); s.cap = None
        else:
            s.still = None; s.cap = cv2.VideoCapture(p + '.mp4'); s.fps = s.cap.get(cv2.CAP_PROP_FPS) or 24
            s.n = int(s.cap.get(cv2.CAP_PROP_FRAME_COUNT)); s.cache = {}
    def at(s, t):
        if s.still is not None: return s.still
        i = max(0, min(int(round(t * s.fps)), s.n - 1))
        if i not in s.cache:
            s.cap.set(cv2.CAP_PROP_POS_FRAMES, i); ok, f = s.cap.read()
            s.cache = {i: cover(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))}
        return s.cache[i]

def cover(f):
    h, w = f.shape[:2]; k = max(W / w, H / h)
    f = cv2.resize(f, (round(w * k), round(h * k)), interpolation=cv2.INTER_LANCZOS4)
    y = (f.shape[0] - H) // 2; x = (f.shape[1] - W) // 2; return f[y:y + H, x:x + W]

def zoom(arr, z):
    if z <= 1.001: return arr
    cw, ch = W / z, H / z; x0, y0 = (W - cw) / 2, (H - ch) / 2
    return cv2.resize(arr[int(y0):int(y0 + ch), int(x0):int(x0 + cw)], (W, H), interpolation=cv2.INTER_CUBIC)

srcs = {n: Src(n) for n in {s[0] for s in SEGS}}
starts = []; t = 0
for s in SEGS: starts.append(t); t += s[2]
DUR = t
os.makedirs(os.path.join(HERE, 'sortie'), exist_ok=True)
tmp = os.path.join(HERE, 'sortie', f'_v{V}.mp4')
proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                         '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
caps = {}
for fi in range(int(DUR * FPS)):
    t = fi / FPS
    k = max(i for i, st in enumerate(starts) if st <= t + 1e-6)
    name, off, d, sp, cap = SEGS[k]; lt = t - starts[k]
    arr = srcs[name].at(off + lt * sp)
    z = 1.0 + 0.035 * lt / d                                   # léger zoom avant, comme un téléphone qui s'approche
    if k > 0: z *= 1 + 0.03 * math.exp(-lt / 0.08)              # petite secousse de coupe
    arr = zoom(arr, z)
    fr = Image.fromarray(arr).convert('RGBA')
    fr.alpha_composite(BADGE, (48, int(H * 0.075)))
    if cap:
        if cap not in caps: caps[cap] = pill(cap[1:].upper(), 50, INK + (215,), CREAM) if cap.startswith('#') else tiktok_text(cap.split('|'))
        im = caps[cap]; fr.alpha_composite(im, ((W - im.width) // 2, int(H * 0.30)))
    if k == len(SEGS) - 1:                                      # offre sur le dernier plan
        a = min(1, max(0, (lt - 0.15) / 0.25))
        p1 = pill(OFFER, 78, ROSE + (255,), (255, 255, 255)); p2 = pill(OFFER2, 40, (255, 255, 255, 235), INK)
        for p, y in ((p1, 0.58), (p2, 0.66)):
            q = p.copy(); q.putalpha(q.split()[3].point(lambda v: int(v * a))); fr.alpha_composite(q, ((W - q.width) // 2, int(H * y)))
    out = np.asarray(fr.convert('RGB')).astype(np.int16)
    out = np.clip(out + np.random.default_rng(fi).normal(0, 3, (H, W, 1)).astype(np.int16), 0, 255).astype(np.uint8)
    proc.stdin.write(out.tobytes())
proc.stdin.close(); proc.wait()
# bande son : musique libre générée (Tom pourra la remplacer dans Meta)
music = os.path.join(HERE, '..', 'kling-variantes', 'audio', 'bande-son-defile.m4a')
final = os.path.join(HERE, 'sortie', f'ciepelle-ugc-{V}.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-stream_loop', '-1', '-i', music, '-map', '0:v', '-map', '1:a', '-shortest',
                '-af', f'volume=-4dB,afade=t=out:st={DUR - 0.6:.2f}:d=0.6', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', final], check=True)
os.remove(tmp); print('ok', final, round(DUR, 2), 's')
