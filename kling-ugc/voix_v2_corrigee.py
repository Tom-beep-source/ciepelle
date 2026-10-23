# Voix off v2 (celle de la pub en ligne) : on garde TOUT, sauf deux phrases devenues fausses,
# remplacées par la même voix Zephyr (prise 3 du 22/10) :
#   « Rozmiar uniwersalny. »                          -> « Pasuje od S do XL. »
#   « Dwie pary za sto czterdzieści dziewięć złotych. » -> « Kup dwie pary, trzecią masz gratis! »
# Usage : python3 voix_v2_corrigee.py <prise3.wav>
import sys, os, subprocess, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SR = 24000
def load(f):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(r, np.float32).astype(np.float64)
def rms(x): return np.sqrt((x ** 2).mean() + 1e-12)
def speech_bounds(x, thr_db=-38, win=0.01):
    n = int(win * SR); e = np.array([20 * np.log10(rms(x[i:i + n])) for i in range(0, len(x) - n, n)])
    idx = np.where(e > thr_db)[0]; return idx[0] * n, (idx[-1] + 1) * n
v2 = load(os.path.join(HERE, 'audio', 'voixoff-zephyr-v2.wav')); t3 = load(sys.argv[1])
S = lambda a, b, x: x[int(a * SR):int(b * SR)]
# zones de la prise 3 contenant la phrase (bornes dans des silences), puis recadrage précis sur la parole
def phrase(a, b, pitch=1.0):
    x = load(sys.argv[1]) if pitch == 1.0 else np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', sys.argv[1], '-af',
        f'rubberband=pitch={pitch:.4f}:pitchq=quality:formant=preserved', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
        capture_output=True, check=True).stdout, np.float32).astype(np.float64)
    seg = S(a, b, x); s, e = speech_bounds(seg); e = min(len(seg), e + int(0.05 * SR)); y = seg[s:e].copy()
    n1, n2 = int(0.008 * SR), int(0.04 * SR); y[:n1] *= np.linspace(0, 1, n1); y[-n2:] *= np.linspace(1, 0, n2); return y
TA = [float(x) for x in sys.argv[2].split(',')]; OF = [float(x) for x in sys.argv[3].split(',')]
taille = phrase(*TA); offre = phrase(*OF)
# même niveau que les phrases remplacées
taille *= rms(S(12.70, 14.15, v2)) / rms(taille); offre *= rms(S(17.30, 20.12, v2)) / rms(offre)
sil = lambda d: np.zeros(int(d * SR))
# v2 : « …otula brzuch » finit vers 12,45 s ; « Rozmiar uniwersalny » 12,70–14,15 ; « Do wyboru » reprend à 14,29 s ;
#      « …albo szary » finit vers 17,25 s ; « Dwie pary… » 17,30–20,12.
pre = S(0, 12.62, v2); s0, _ = speech_bounds(S(12.62, 14.24, v2))
mid = S(14.24, 17.27, v2)
gap_a = 12.70 - 12.62                       # même respiration avant la phrase qu'à l'origine
out = np.concatenate([pre, sil(gap_a), taille, sil(0.10), mid, sil(0.05), offre, sil(0.6)])
# micro-fondus aux raccords (5 ms) pour éviter tout clic
def fade(x, at, d=0.005):
    i = int(at * SR); n = int(d * SR); x[i - n:i] *= np.linspace(1, 0, n); x[i:i + n] *= np.linspace(0, 1, n)
t_taille = len(pre) / SR + gap_a; t_mid = t_taille + len(taille) / SR + 0.10; t_offre = t_mid + len(mid) / SR + 0.05
for at in (len(pre) / SR, t_mid, t_mid + len(mid) / SR): fade(out, at)
pk = np.abs(out).max()
if pk > 0.97: out *= 0.97 / pk
dst = os.path.join(HERE, 'audio', 'voixoff-zephyr-v2-corrigee.wav')
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'f64le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'pcm_s16le', dst], stdin=subprocess.PIPE)
p.communicate(out.astype(np.float64).tobytes())
info = {'duree': round(len(out) / SR, 3), 'taille_debut': round(t_taille, 3), 'taille_fin': round(t_taille + len(taille) / SR, 3),
        'do_wyboru_debut': round(t_mid + 0.05, 3), 'decalage_apres_taille': round(t_mid - 14.24, 3),
        'offre_debut': round(t_offre, 3), 'offre_fin': round(t_offre + len(offre) / SR, 3)}
json.dump(info, open(os.path.join(HERE, 'audio', 'voixoff-zephyr-v2-corrigee.json'), 'w'), indent=1); print(info)
