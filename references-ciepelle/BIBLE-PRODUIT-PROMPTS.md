# Ciepelle : fiche produit pour les prompts (Higgsfield)

Basée sur les 13 photos Shopify du produit, numérotées 00 à 12 dans ce dossier (fichiers `.jpg`, plus `planche-contact.jpg`).

## 1. Ce que l'IA doit reproduire

À coller tel quel au début de chaque prompt (en anglais, les modèles le comprennent mieux) :

```
PRODUCT: women's fleece-lined thermal tights with a "fake translucent" effect.
Outer layer: thin sheer smoky nylon, soft matte finish, very slight sheen.
Inner layer: thick plush brushed fleece in a warm golden-camel color, only visible when the waistband is folded down.
Worn look: from the outside the legs look like they are in classic sheer tights, smooth and even, no fleece texture visible.
High-rise wide flat waistband reaching the navel, single thin vertical seam at the center back, flat gusset seam, fully footed with reinforced toe.
```

Couleur, une ligne au choix :
- **Cielisty (chair)** : `"nude" variant: reads as sheer warm taupe / light smoky-brown tights over skin, slightly darker and more uniform than bare skin`
- **Czarny (noir)** : `black variant: reads as sheer smoky black tights, skin tone faintly visible through the knees and thighs`

À ajouter à chaque prompt (négatif) :
```
no grey tights, no glossy shine, no opaque leggings look, no fishnet, no pattern, no logo, no text, no brand label, no visible bulk or wrinkles from the fleece, legs not unnaturally slim
```

**Pourquoi cette précision :** sur vos photos, la version « chair » n'est **pas** une peau nue parfaite, c'est un voile taupe fumé. Si l'IA la rend comme des jambes nues, la pub promet mieux que le produit, et vous aurez des retours.

## 2. Quelles photos donner en référence

| Usage | Photos à charger | Remarque |
|---|---|---|
| Doublure polaire (retournement) | **02, 05, 11** | Le plan le plus convaincant, à mettre dans chaque pub |
| Porté chair, en entier | **10**, 08 (recadrée) | Recadrer 08 pour enlever les traits roses dessinés |
| Porté noir | **06, 00, 09** | |
| Taille haute / silhouette | **03, 04** | |
| Ambiance rue / bottes | **01, 06** | |
| ⛔ Ne pas utiliser | **07, 12** | Elles montrent un collant **gris**, une couleur que vous ne vendez pas |

Mettez 2 ou 3 photos maximum par génération : une pour la matière, une pour le rendu porté. Au-delà, le résultat se dilue.

**Visage des avatars :** n'utilisez pas la femme de la photo 01 (photo fournisseur, vous n'avez pas les droits sur son visage). Prenez un avatar de la bibliothèque Higgsfield ou un visage généré.

## 3. Méthode dans Higgsfield

1. **Image fixe d'abord :** générez avec un modèle qui accepte des images de référence, avec la fiche ci-dessus + la scène. Gardez seulement les images où le collant est fidèle à vos photos.
2. **Animation :** passez l'image validée en image-to-video, en plans de 3 à 5 secondes.
3. **Avatar qui parle :** vérifiez que l'outil avatar gère bien le **polonais** et la synchronisation des lèvres, sinon passez en voix off + sous-titres.
4. **Montage :** CapCut, sous-titres polonais, 9:16.

## 4. Règles pour les avatars dans les pubs Meta

Les avatars sont possibles, à condition qu'ils **présentent** le produit sans **se faire passer pour des clientes** :
- ✅ « Zobacz, co jest w środku. », « Tak wyglądają z bliska. », « Masz do wyboru 80, 220 albo 300 g. »
- ❌ « Kupiłam je… », « Noszę je od dwóch zim… », « Koleżanka mnie zapytała… », « Najlepsze rajstopy, jakie miałam… »
- Activez la mention **contenu IA** de Meta à la création de la pub. Sur Meta, un faux témoignage par une personne générée peut entraîner le rejet de la pub. En Pologne, l'autorité de la consommation (UOKiK) poursuit activement les faux avis.

## 5. Pilote : script 1 réécrit pour avatar, « Nie, to nie gołe nogi »

Durée 20 s, 9:16. Avatar : femme de 28–35 ans, cheveux châtains, manteau camel, robe en maille.

| Plan | Prompt image (Higgsfield) | Voix PL / texte à l'écran |
|---|---|---|
| 1 · 0–3 s | `[FICHE PRODUIT] + "nude" line. Vertical 9:16 smartphone UGC shot, winter morning at a Polish city tram stop, light frost, overcast soft daylight. Woman 30 y.o. in camel wool coat and short knit dress, legs in the tights, black ankle boots. Framing from waist down, slightly low angle. Natural, unpolished, handheld look. [NEGATIVE]` · refs 10 + 01 | **Napis:** „Grudzień. Sukienka. Gołe nogi? 🥶” |
| 2 · 3–8 s | `Same woman, same outfit, close-up on her knee: she pinches the sheer fabric between two fingers and gently pulls it away from the skin, showing it is tights. [FICHE] [NEGATIVE]` · refs 00 *(pour le geste de pincement)* + 10 *(pour la couleur chair)* | „Nie – to rajstopy. Tylko że w środku mają polar.” |
| 3 · 8–14 s | `Indoors, warm lamp light, beige knit blanket. Close-up from above: the waistband of the tights folded down over the thighs, revealing the thick golden-camel plush fleece lining, sheer smoky outer layer below. Hand brushing the fleece. [FICHE] [NEGATIVE]` · refs **02 + 05** | „Z zewnątrz wyglądają jak cienkie rajstopy, a od środka jest miękki polar.” |
| 4 · 14–18 s | Avatar face caméra, intérieur chaleureux, plan buste (avatar parlant) | „Do wyboru: 80, 220 albo 300 gramów. Cielisty albo czarny.” |
| 5 · 18–20 s | Plan packshot : les deux couleurs posées côte à côte sur un lit blanc · refs 10 + 09 | **Napis:** „Ciepelle · darmowa dostawa · 14 dni na zwrot” |

Si ce pilote vous plaît une fois généré, je décline les 5 autres scripts de la même façon.
