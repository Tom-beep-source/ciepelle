# Pub v5 (22/10) : EXACTEMENT la pub en ligne (ugc3 : mêmes plans, même voix v2, même musique),
# seules deux phrases fausses changent (voix + texte à l'écran) :
#   « Rozmiar uniwersalny / ok. 40–70 kg »  -> voix « Pasuje od S do XL » + texte « Jeden rozmiar: S–XL / ok. 40–90 kg »
#   « Dwie pary za 149 zł »                 -> voix « Kup dwie pary, trzecią masz gratis! » + carte 2 + 1 GRATIS / 3 pary za 198 zł
# Les durées des plans suivent les nouveaux temps de la voix (audio/voixoff-zephyr-v2-corrigee.json).
import os, json, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
V = json.load(open(os.path.join(HERE, 'audio', 'voixoff-zephyr-v2-corrigee.json')))
src = open(os.path.join(HERE, 'ugc3.py'), encoding='utf-8').read()

c5_start = 12.50                                    # inchangé : C5 commence à 12,50 s comme dans la pub en ligne
dw = V['do_wyboru_debut'] - c5_start                # « Do wyboru » (était 1,79 s après le début du plan)
d = V['decalage_apres_taille']                      # décalage de tout ce qui suit la phrase sur la taille
o4_start = V['offre_debut'] - 0.10                  # la carte d'offre arrive avec « Kup dwie pary »
if 'cielisty' in V:                                 # v5b : plans couleurs calés sur les mots de la nouvelle voix
    c5_len = V['cielisty'] - 0.05 - c5_start; v1_len = V['czarny'] - V['cielisty']; v2_len = V['szary'] - V['czarny']
else:
    c5_len = 2.65 + d; v1_len = 0.75; v2_len = 0.6
v3_len = o4_start - (c5_start + c5_len + v1_len + v2_len)
o4_len = V['duree'] - o4_start
trz = V.get('trzecia', 0.91)                        # « trzecią » après le début de l'offre

new_segs = f"""SEGS = [  # v5 : plans de la pub en ligne, voix v2 corrigée
  ('C1', 0.0, 4.75, 1.0, [(0.0, 'Wyglądają jak cienkie…', None), (2.95, '…a w środku polar!', None)], {{}}),
  ('K3', 0.6, 2.35, 1.1, [(0.05, 'Trzyma ciepło', None), (0.95, 'Chroni przed chłodem', None)], {{}}),
  ('C2', 0.0, 2.35, 1.0, [(0.05, 'Bardzo elastyczne', None), (1.0, 'Ładnie przylegają', 'do nóg')], {{}}),
  ('C3', 0.0, 3.05, 1.0, [(0.06, 'Wysoki stan', 'nie zjeżdża'), (2.13, 'Otula brzuch', None)], {{'z0': 1.45, 'cy': .32}}),
  ('C5', 0.0, {c5_len:.3f}, 1.0, [({V['taille_debut'] - c5_start - 0.02:.3f}, 'Jeden rozmiar: S–XL', 'ok. 40–90 kg'), ({dw:.3f}, 'Do wyboru: 3 kolory', None)], {{}}),
  ('V1', 2.98, {v1_len:.3f}, 1.2, 'cielisty', {{'tag': 1}}), ('V2', 0.23, {v2_len:.3f}, 1.2, 'czarny', {{'tag': 1}}), ('V3', 0.27, {v3_len:.3f}, 1.2, 'szary', {{'tag': 1}}),
  ('O4', 0.8, {o4_len:.3f}, 1.0, None, {{'offer': 1}})]
"""
a = src.index('SEGS = ['); b = src.index("N = 'vo'")
src = src[:a] + new_segs + src[b:]

old_of = src[src.index("OF1 = pill('2 pary za 149 zł'"):src.index("for fi in range(NF):")]
src = src.replace(old_of, """OF1 = pill('2 + 1 GRATIS', 92, ROSE + (255,), (255, 255, 255)); OF2 = pill('trzecia para za 0 zł', 54, (255, 255, 255, 245), INK)
OF3 = pill('3 pary za 198 zł', 50, (255, 255, 255, 245), INK)
OF4 = pill('darmowa dostawa · 14 dni na zwrot', 36, (255, 255, 255, 235), INK, pad=(30, 16))
OF0 = caption('Kliknij i zamów', 62)
""")
old_offer = src[src.index("        a = (lt - .1) / .2; b = (lt - .35) / .2"):src.index("    out = np.asarray(fr.convert('RGB'))")]
src = src.replace(old_offer, f"""        for im, y, t0 in ((OF1, .52, 0.10), (OF2, .605, {trz + 0.10:.3f}), (OF0, .43, {V['offre_fin'] - o4_start - 0.45:.3f}),
                          (OF3, .68, {V['offre_fin'] - o4_start - 0.25:.3f}), (OF4, .745, {V['offre_fin'] - o4_start - 0.05:.3f})):
            p = (lt - t0) / .18
            if p <= 0: continue
            q = pop(im, p); fr.alpha_composite(q, ((W - q.width) // 2, int(H * y)))
""")
src = src.replace("os.path.join(HERE, 'sortie', '_vo.mp4')", "os.path.join(HERE, 'v5', '_vo.mp4')")
src = src.replace("os.makedirs(os.path.join(HERE, 'sortie'), exist_ok=True)", "os.makedirs(os.path.join(HERE, 'v5'), exist_ok=True)")
src = src.replace("os.path.join(HERE, 'sortie', 'ciepelle-ugc-voixoff-SANS-SON.mp4')", "os.path.join(HERE, 'v5', 'ciepelle-ugc-v5-SANS-SON.mp4')")
src = src.replace("os.path.join(HERE, 'sortie', 'timing-voixoff.json')", "os.path.join(HERE, 'v5', 'timing-v5.json')")
assert "149" not in src and "40–70" not in src and "uniwersalny" not in src
open(os.path.join(HERE, 'v5', '_ugc5_genere.py') if os.path.isdir(os.path.join(HERE, 'v5')) else os.devnull, 'w').write(src)
exec(compile(src, 'ugc5', 'exec'), {'__file__': os.path.join(HERE, 'ugc3.py'), '__name__': '__main__'})
