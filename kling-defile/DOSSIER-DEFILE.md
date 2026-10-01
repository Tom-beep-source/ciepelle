# Ciepelle : « Pokaz zimowy », le défilé (pub Meta 9:16, 16 s)

## 1. Ce que disent les pubs qui marchent (TrendTrack, 6 pays)

| Pub | Pays | Résultat | Ce qu'on en retient |
|---|---|---|---|
| Feelwonder | DE | 10,9 M de personnes atteintes, 790 jours | **Polaire montré dès la 1ʳᵉ seconde**, plans rapides d'environ 1 s, logo en petit pendant toute la vidéo, musique sans voix |
| Collant Leggs | FR | 7,1 M, 818 jours | Créatrice qui montre les couleurs, ton naturel |
| Le Collant Frenchie | FR | 4,0 M | Fondatrice face caméra, « élégantes l'hiver sans avoir froid » |
| FleeceWereld | NL | 981 k | Une phrase sous-titrée par plan, plusieurs femmes, polaire montré vers 15 s, offre « 2+1 » |
| Cose Online | IT | 377 k | Accroche texte, pincement du collant, polaire montré deux fois, lumière de soleil |
| Veritas | BE | 127 jours | **Uniquement des jambes, sans visage**, lumière naturelle, ambiance cocooning, musique seule |
| Magic Curve | US / GB | 435 variantes de la même pub | « This isn't my skin », la femme soulève sa robe pour montrer le collant |

**Conclusions :**
1. Montrer le polaire **tôt**.
2. Le geste du pincement, « ce n'est pas ma peau ».
3. Les jambes seules fonctionnent.
4. Le logo présent en continu.
5. Une offre de lot.
6. **Personne ne fait de défilé sur ce produit** : c'est notre différence.

On reprend leurs **structures**, pas leurs vidéos ni leurs textes. Une atteinte aux droits peut faire suspendre votre compte publicitaire.

## 2. Règles Meta respectées
- Les 3 premières secondes portent près de la moitié de la valeur d'une pub vidéo (étude Meta + Nielsen). On ouvre donc sur l'accroche, pas sur le logo.
- Logo visible tôt (petit, en haut) : c'est 25 % de mémorisation en plus. Le logo revient en grand à la fin.
- Textes placés hors des zones masquées par les Reels : pas dans les 14 % du haut, pas dans les 35 % du bas.
- Pensé pour être regardé avec le son (70 à 80 % des Reels le sont) et compréhensible sans le son grâce aux textes.
- « Presque sexy » sans risque : marche assurée, talons, mini-jupes, cadrage de face de la jupe aux pieds. **Pas de gros plan sur les fesses ni l'entrejambe** : Meta restreint ces images aux plus de 18 ans et les diffuse moins.
- Mention IA cochée dans le Gestionnaire de publicités.

## 3. Le montage final (15 s, 126 BPM)

Chaque coupe tombe sur un temps de la musique, et chaque bruit de talon tombe sur le pas réel du plan (pas détectés image par image dans les vidéos Kling).

| Temps | Plan (vraie vidéo Kling) | Texte (PL) | Son |
|---|---|---|---|
| 0–1,9 s | Femme n°1 (cielisty) qui avance vers la caméra | « Wyglądają jak gołe nogi… » | Beat de défilé + talons qui résonnent |
| 1,9–3,8 s | Mains qui écartent le collant retourné : le polaire | « …a w środku polar. » | idem |
| 3,8–5,7 s | Femme n°1, suite du défilé | CIELISTY | idem |
| 5,7–7,6 s | Femme n°2 (czarny, bottines) | CZARNY | idem |
| 7,6–9,5 s | Femme n°3 (szary, robe-pull) | SZARY | idem |
| 9,5–12,3 s | Vue de dos : elle sort par les portes ouvertes, dans la neige, cheveux soulevés par le vent | « A za drzwiami… » puis « zima. » au passage du seuil | **Le son s'éloigne** (−9 dB, aigus coupés, plus d'écho), puis vent d'hiver et pas étouffés dans la neige |
| 12,3–12,5 s | Noir | — | « Whoosh » |
| 12,5–15 s | **Logo Ciepelle** qui frappe au centre exact de l'image, puis « RAJSTOPY Z POLAREM · 80 g · 220 g · 300 g » | — | Impact sourd + longue résonance |

Petit logo permanent en haut, dans une pastille encre (lisible sur tous les fonds). Textes dans des bandeaux encre, hors des zones masquées par les Reels.

La musique est **originale, composée par code** pour cette pub : c'est donc 100 % libre de droits. Si elle ne vous plaît pas, téléchargez un morceau de la **Meta Sound Collection** (gratuit, autorisé en pub) et je le remonte avec le même traitement du son.

## 4. Fichiers
- **`pub-defile-ciepelle.mp4`** : la pub à importer dans Meta (1080×1920, 24 i/s, son −14,5 LUFS, 22 Mo).
- `montage/controle-montage.jpg` : planche de contrôle (11 images de la pub).
- `clips/` : les 5 vidéos Kling brutes, sans filigrane (V1, VF, V2, V3, VS), et leurs planches `*_strip.jpg`. Les liens Kling expirent en 24 h : ces copies sont les seules.
- `montage/plan.py` (calage tempo / pas), `montage/montage.py` (rendu), `audio/music.py` (musique + design sonore). Pour refaire : `python3 montage/plan.py`, puis `audio/music.py`, puis `montage/montage.py` (chacun depuis son dossier).
- `animatique/` : l'ancienne version en plans fixes, remplacée.

## 5. Ce qui a été généré (prompts exacts, pour refaire un plan)

### Images de départ (Nano Banana Pro, 1 image chacune ≈ 20 crédits)
- **W2 (czarny)**, références : W1a + photo 06.
  > Same runway hall, same soft daylight from the tall windows, same knee-height camera, lens and framing as the first image. A different model walks toward camera mid-stride, relaxed and confident, hips leading, wearing a short charcoal knit mini dress and black leather ankle boots with a slim heel, and sheer smoky black fleece-lined tights exactly like the second image: skin tone faintly visible through the nylon at the knees and thighs, soft matte finish. 35mm film grain, candid, unretouched. No face, no upper body, no text, no logo.
- **W3 (szary)**, références : W1a + photo 12. Même prompt, avec une robe-pull en maille crème, des escarpins noirs et « sheer cool grey fleece-lined tights exactly like the second image ».
- **SORTIE**, référence : W1a.
  > Same hall seen from behind: at the far end of the concrete runway two tall glass doors stand wide open onto a snowy courtyard, heavy snow falling outside and a few flakes drifting in over the floor, cold blue daylight outside against the warm hall. The same model, framed from the waist down from behind, in the oatmeal mini skirt, sheer warm taupe tights and black heels, walks unhurried toward the open doors. 35mm film grain, candid. No face, no text, no logo.

### Vidéos (Kling 3.0, image vers vidéo, 1080p, 5 s, un seul plan continu, `prefer_multi_shots=false`)
- **V1 / V2 / V3 (défilé) :**
  > The model keeps walking toward the camera along the concrete runway in an unhurried, confident runway walk: hips leading, each heel landing directly in front of the other, heel first then rolling to the toe, relaxed knees, hands loose by her sides. The camera dollies backward at the same speed at knee height, keeping her framed from the skirt hem to the shoes. Soft daylight from the tall windows sweeps across her legs. The tights stay smooth and identical in colour, natural skin tone through the sheer nylon, no morphing, no extra limbs, stable feet. Sound: only crisp high-heel clicks on concrete echoing in a large empty hall, no music, no voices.
- **VF (polaire), Kling 3.0 Turbo, sans son :**
  > Static close-up. The hands slowly stretch the inside-out waistband a little wider; the plush golden fleece shifts softly and catches the window light, fine fibres visible. Subtle natural hand micro-movements, no morphing.
- **VS (sortie) :**
  > She walks away from the camera through the open glass doors and steps out into the falling snow without slowing down, snowflakes swirling around her legs; the camera stays still inside the hall as she gets smaller in the bright winter light. Sound: heel clicks echoing in the hall, then muffled steps in fresh snow and a soft winter wind.

### Crédits dépensés
- Images de départ Nano Banana Pro : W1a, W1b, Fa, Fb, W2, W3, SORTIE (20 crédits chacune).
- Vidéos : V1, V2, V3, VS (Kling 3.0, 1080p, son : 60 crédits chacune), VF (Kling 3.0 Turbo : 50 crédits).
- **Solde Kling après la pub : 295 crédits.** Aucun plan n'a dû être refait.

Les 5 vidéos ont été vérifiées image par image : pas de jambes qui se croisent mal, pas de pied qui glisse, teinte du collant stable du début à la fin de chaque plan.

## 6. Ce qui est garanti, ce qui ne l'est pas
- **Garanti** : la bande-son, le montage, le logo, les textes, et la fidélité du collant (je contrôle chaque image).
- **Pas garanti à 100 %** : la génération vidéo IA reste aléatoire, en particulier sur la marche (jambes, pieds). On réduit le risque avec des images de départ validées, des mouvements de caméra simples et des plans de 5 s, mais un plan peut devoir être refait.
