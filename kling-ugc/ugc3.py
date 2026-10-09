# Montage dynamique style créatrice UGC (TikTok / Reels) : coupes rapides, zoom d'impact, transition « swipe »,
# sous-titres mot par mot (même texte que la future voix off polonaise), bruitages, offre finale.
# Usage : python3 ugc2.py 1|2|3  -> sortie/ciepelle-ugc2-N.mp4
import sys, os, math, subprocess, numpy as np, cv2, json
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__)); C = os.path.join(HERE, 'clips')
SANS = os.path.join(HERE, '..', 'kling-variantes', 'assets', 'Manrope.ttf')
SERIF = os.path.join(HERE, '..', 'kling-variantes', 'assets', 'DMSerifDisplay-Regular.ttf')
ROSE = (181, 84, 111); INK = (34, 27, 31); CREAM = (251, 246, 242); YEL = (255, 214, 64)
# plan, début (s), durée (s), vitesse, texte (morceaux séparés par « / », affichés à la suite), options
# Version « voix off » : mots-clés à l'écran synchronisés avec la voix, vidéo SANS son (Tom ajoute voix + musique).
# plan, début (s), durée (s), vitesse, [(instant dans le plan, mot-clé, petite ligne)], options
SEGS = [
  ('C1', 0.0, 2.6, 1.0, [(0.0, 'Wyglądają jak cienkie…', None), (1.25, '…a w środku polar!', None)], {}),
  ('VF', 0.5, 1.8, 1.0, [(0.1, 'Trzyma ciepło', None)], {}),
  ('K3', 0.6, 1.8, 1.1, [(0.1, 'Chroni przed chłodem', None)], {}),
  ('C2', 0.0, 2.4, 1.0, [(0.2, 'Bardzo elastyczne', None)], {}),
  ('H1', 0.5, 2.0, 1.0, [(0.1, 'Ładnie przylegają', 'do nóg')], {}),
  ('C3', 0.0, 2.4, 1.0, [(0.0, 'Wysoki stan', 'nie zjeżdża'), (1.2, 'Otula brzuch', None)], {'z0': 1.45, 'cy': .32}),
  ('C5', 0.0, 2.2, 1.0, [(0.1, 'Rozmiar uniwersalny', 'ok. 40–70 kg')], {}),
  ('V1', 2.98, 0.8, 1.2, 'cielisty', {'tag': 1}), ('V2', 0.23, 0.8, 1.2, 'czarny', {'tag': 1}), ('V3', 0.27, 0.8, 1.2, 'szary', {'tag': 1}),
  ('O4', 0.8, 3.2, 1.0, None, {'offer': 1})]
N = 'vo'
def font(s, w=800):
    f = ImageFont.truetype(SANS, s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def wrap(text, f, maxw):
    d0 = ImageDraw.Draw(Image.new('L', (1, 1))); lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d0.textlength(t, font=f) > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]
def caption(text, size=70):
    f = font(size); d0 = ImageDraw.Draw(Image.new('L', (1, 1))); lines = wrap(text, f, 900); lh = int(size * 1.2)
    ws = [d0.textlength(l, font=f) for l in lines]
    im = Image.new('RGBA', (int(max(ws)) + 40, lh * len(lines) + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (l, w) in enumerate(zip(lines, ws)):
        d.text(((im.width - w) / 2, 12 + i * lh), l, font=f, fill=(255, 255, 255), stroke_width=8, stroke_fill=(0, 0, 0))
    return im
def pill(text, size, bg, fg, pad=(36, 20)):
    f = font(size); d0 = ImageDraw.Draw(Image.new('L', (1, 1))); w = d0.textlength(text, font=f)
    im = Image.new('RGBA', (int(w + 2 * pad[0]), int(size * 1.15 + 2 * pad[1])), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=im.height // 2, fill=bg)
    d.text((pad[0], pad[1] - size * 0.08), text, font=f, fill=fg); return im
def keyword(text, sub=None):
    f = font(76, 850); d0 = ImageDraw.Draw(Image.new('L', (1, 1))); w = d0.textlength(text, font=f)
    px, py = 34, 18; bw, bh = int(w + 2 * px), int(76 * 1.18 + 2 * py)
    sw = 0
    if sub: fs = font(46, 750); sw = d0.textlength(sub, font=fs)
    im = Image.new('RGBA', (int(max(bw, sw + 40)) + 20, bh + (80 if sub else 0) + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x0 = (im.width - bw) // 2; d.rounded_rectangle([x0 + 6, 16, x0 + bw + 6, bh + 16], radius=22, fill=(0, 0, 0, 90))
    d.rounded_rectangle([x0, 10, x0 + bw, bh + 10], radius=22, fill=YEL + (255,)); d.text((x0 + px, 10 + py - 76 * .08), text, font=f, fill=INK)
    if sub: d.text(((im.width - sw) / 2, bh + 26), sub, font=fs, fill=(255, 255, 255), stroke_width=6, stroke_fill=(0, 0, 0))
    return im
def badge():
    f = ImageFont.truetype(SERIF, 42); w = ImageDraw.Draw(Image.new('L', (1, 1))).textlength('Ciepelle', font=f)
    im = Image.new('RGBA', (int(w + 50), 66), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, 65], radius=33, fill=INK + (170,)); d.text((25, 7), 'Ciepelle', font=f, fill=CREAM); return im
BADGE = badge()
def pop(im, p):
    e = 1 - (1 - min(1, max(0, p))) ** 3; s = .85 + .15 * e
    out = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    if e < 1: out.putalpha(out.split()[3].point(lambda v: int(v * e)))
    return out

def cover(f):
    h, w = f.shape[:2]; k = max(W / w, H / h)
    f = cv2.resize(f, (round(w * k), round(h * k)), interpolation=cv2.INTER_AREA if k < 1 else cv2.INTER_CUBIC)
    y = (f.shape[0] - H) // 2; x = (f.shape[1] - W) // 2; return f[y:y + H, x:x + W]
class Src:
    def __init__(s, name, lo=0, hi=1e9):
        p = os.path.join(C, name); s.lo = lo
        for ext in ('.png', '.jpg'):
            if os.path.exists(p + ext): s.still = cover(cv2.cvtColor(cv2.imread(p + ext), cv2.COLOR_BGR2RGB)); return
        s.still = None; cap = cv2.VideoCapture(p + '.mp4'); s.fps = cap.get(cv2.CAP_PROP_FPS) or 24; s.frames = []
        s.i0 = int(lo * s.fps); k = 0
        while True:
            ok, f = cap.read()
            if not ok or k > hi * s.fps + 2: break
            if k >= s.i0: s.frames.append(f)   # on ne garde en mémoire que la partie du plan utilisée
            k += 1
    def at(s, t):
        if s.still is not None: return s.still
        i = max(0, min(int(t * s.fps) - s.i0, len(s.frames) - 1))
        return cover(cv2.cvtColor(s.frames[i], cv2.COLOR_BGR2RGB))
def zoom(arr, z, cx=.5, cy=.5):
    if z <= 1.001: return arr
    cw, ch = W / z, H / z; x0 = min(max(cx * W - cw / 2, 0), W - cw); y0 = min(max(cy * H - ch / 2, 0), H - ch)
    return cv2.resize(arr[int(y0):int(y0 + ch), int(x0):int(x0 + cw)], (W, H), interpolation=cv2.INTER_LINEAR)

_rng = {}
for _s in SEGS:
    lo, hi = _rng.get(_s[0], (1e9, 0)); _rng[_s[0]] = (min(lo, _s[1]), max(hi, _s[1] + _s[2] * _s[3]))
srcs = {n: Src(n, *_rng[n]) for n in _rng}
starts = []; t = 0
for s in SEGS: starts.append(t); t += s[2]
DUR = t; NF = int(DUR * FPS)
os.makedirs(os.path.join(HERE, 'sortie'), exist_ok=True)
tmp = os.path.join(HERE, 'sortie', '_vo.mp4')
proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                         '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
cache = {}; cuts = starts[1:]
OF1 = pill('2 pary za 149 zł', 82, ROSE + (255,), (255, 255, 255)); OF2 = pill('220 g · darmowa dostawa · 14 dni na zwrot', 38, (255, 255, 255, 240), INK)
OF0 = caption('Kliknij i zamów', 58)
for fi in range(NF):
    t = fi / FPS; k = max(i for i, st in enumerate(starts) if st <= t + 1e-6)
    name, off, d, sp, txt, op = SEGS[k]; lt = t - starts[k]
    arr = srcs[name].at(off + lt * sp)
    z = op.get('z0', 1.04) + op.get('push', .06) * lt / d                       # léger zoom avant continu
    if k > 0: z *= 1 + .10 * math.exp(-lt / .07)                 # zoom d'impact à chaque coupe
    arr = zoom(arr, z, cy=op.get('cy', .5))
    if k > 0 and lt < 3 / FPS:                                   # « swipe » : flou de mouvement sur 3 images
        kk = int(90 * (1 - lt * FPS / 3)) + 1; arr = cv2.filter2D(arr, -1, np.ones((1, kk), np.float32) / kk)
    fr = Image.fromarray(arr).convert('RGBA'); fr.alpha_composite(BADGE, (46, int(H * .075)))
    if txt and op.get('tag'):
        im = pill(txt.upper(), 54, INK + (220,), CREAM); fr.alpha_composite(pop(im, lt / .1), ((W - im.width) // 2, int(H * .30)))
    elif txt:
        cur = [x for x in txt if x[0] <= lt + 1e-6][-1:] 
        if cur:
            t0, word, sub = cur[0]; key = (word, sub)
            if key not in cache: cache[key] = keyword(word, sub)
            im = cache[key]; fr.alpha_composite(pop(im, (lt - t0) / .12), ((W - im.width) // 2, int(H * .60)))
    if op.get('offer'):
        a = (lt - .1) / .2; b = (lt - .35) / .2; c = (lt - .7) / .2
        for im, y, p in ((OF0, .50, c), (OF1, .58, a), (OF2, .665, b)):
            q = pop(im, p); fr.alpha_composite(q, ((W - q.width) // 2, int(H * y)))
    out = np.asarray(fr.convert('RGB')).astype(np.int16)
    out = np.clip(out + np.random.default_rng(fi).normal(0, 2.5, (H, W, 1)).astype(np.int16), 0, 255).astype(np.uint8)
    proc.stdin.write(out.tobytes())
proc.stdin.close(); proc.wait()
final = os.path.join(HERE, 'sortie', 'ciepelle-ugc-voixoff-SANS-SON.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-c:v', 'copy', '-an', '-movflags', '+faststart', final], check=True); os.remove(tmp)
json.dump([{'plan': s[0], 'debut': round(st, 2), 'fin': round(st + s[2], 2), 'texte': s[4]} for s, st in zip(SEGS, starts)],
          open(os.path.join(HERE, 'sortie', 'timing-voixoff.json'), 'w'), ensure_ascii=False, indent=1)
print('ok', final, round(DUR, 2), 's')
