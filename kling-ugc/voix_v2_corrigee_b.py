# Voix v5b : voix v2 d'origine jusqu'à « …otula brzuch » (0–12,62 s), puis toute la fin d'un seul tenant
# dans la prise 2 (même voix Zephyr) : « Pasuje od S do XL. Do wyboru: cielisty, czarny albo szary.
# Kup dwie pary, trzecią masz gratis! » -> un seul raccord, intonation continue jusqu'à la fin.
# Usage : python3 voix_v2_corrigee_b.py <prise2.wav>
import sys, os, subprocess, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SR = 24000
def load(f):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(r, np.float32).astype(np.float64)
rms = lambda x: np.sqrt((x ** 2).mean() + 1e-12)
v2 = load(os.path.join(HERE, 'audio', 'voixoff-zephyr-v2.wav')); tk = load(sys.argv[1])
S = lambda a, b, x: x[int(a * SR):int(b * SR)].copy()
A, B = 12.73, 19.94 + 0.08                       # prise 2 : début « Pasuje » -> fin « gratis » (+ souffle de fin)
tail = S(A, B, tk)
tail *= rms(S(12.70, 20.12, v2)) / rms(tail)     # même niveau moyen que la fin d'origine remplacée
n1, n2 = int(0.008 * SR), int(0.06 * SR); tail[:n1] *= np.linspace(0, 1, n1); tail[-n2:] *= np.linspace(1, 0, n2)
pre = S(0, 12.62, v2); gap = 0.08
out = np.concatenate([pre, np.zeros(int(gap * SR)), tail, np.zeros(int(1.9 * SR))])
pk = np.abs(out).max(); out *= min(1, 0.97 / pk)
dst = os.path.join(HERE, 'audio', 'voixoff-zephyr-v2-corrigee.wav')
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'f64le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'pcm_s16le', dst], stdin=subprocess.PIPE)
p.communicate(out.tobytes())
o = 12.62 + gap - A                              # temps prise 2 -> temps final
T = lambda t: round(t + o, 3)
info = {'duree': round(len(out) / SR, 3), 'taille_debut': T(12.73), 'taille_fin': T(14.42), 'do_wyboru_debut': T(14.69),
        'cielisty': T(15.45), 'czarny': T(16.22), 'szary': T(16.83), 'offre_debut': T(17.85), 'trzecia': round(18.85 - 17.85, 3),
        'offre_fin': T(19.94), 'decalage_apres_taille': 0}
json.dump(info, open(os.path.join(HERE, 'audio', 'voixoff-zephyr-v2-corrigee.json'), 'w'), indent=1); print(info)
