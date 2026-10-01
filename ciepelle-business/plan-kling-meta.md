# Ciepelle × Kling : méthode pour produire des pubs Meta sans gaspiller de crédits

Recherche faite le 1er octobre 2026. Les sources sont listées en bas.

## 1. Ce que coûte Kling (pour budgéter)

| Action | Coût approximatif |
|---|---|
| Envoyer une photo à Kling, créer un « Element » | Gratuit |
| Image Kling 3.0 Omni (1–2K) | ~2 crédits |
| Vidéo Kling 3.0, 720p, **sans son**, 5 s | ~30 crédits (6 crédits/s) |
| Vidéo Kling 3.0, 720p **avec son**, 5 s | ~45 crédits (9 crédits/s) |
| Vidéo 1080p avec son, 5 s | ~60 crédits |
| **Une génération ratée ou refusée** | **Consomme quand même les crédits** |

Formules : 660 crédits/mois pour ~10 $ (~42 zł), 3 000 crédits pour ~37 $ (~155 zł). Les crédits d'abonnement expirent au bout d'un mois, les recharges au bout de 2 ans. **Votre compte est actuellement à 0 crédit.**

**Conséquence :** la vidéo coûte environ 15 fois plus cher que l'image. On valide donc tout **en image d'abord** (~2 crédits), et on ne lance une vidéo que sur une image approuvée.

---

## 2. Les règles qui marchent (Kling + Meta)

### Côté Kling
1. **Image vers vidéo plutôt que texte vers vidéo.** L'image de départ sert d'ancre : Kling garde le produit, les couleurs et la composition, et n'ajoute que le mouvement. C'est le meilleur moyen d'éviter que le collant change d'un plan à l'autre.
2. **Structure du prompt :** Scène → Sujet → Action → Caméra → Lumière / ambiance. On décrit **ce qui se voit**, pas des idées.
3. **Mouvements de caméra courts et précis :** « slow push-in », « static close-up », « gentle tracking shot ». Pas de mouvement complexe : plus ça bouge, plus le tissu se déforme.
4. **Des plans de 3 à 5 secondes**, un plan égale une idée. On monte ensuite dans CapCut.
5. **Préciser ce qui ne doit pas bouger** : « no shake, fabric texture stays consistent, no morphing, natural hands ». Les mains et les tissus sont les points faibles.
6. **Les références** : 2 ou 3 photos par génération maximum, une pour la matière et une pour le rendu porté. Dans les prompts Kling Omni, on y fait référence avec `图片1`, `图片2`.
7. **Un « Element » produit** : Kling peut mémoriser le collant comme un sujet réutilisable (1 photo principale + 1 à 3 secondaires). C'est gratuit et ça renforce la cohérence d'une pub à l'autre.
8. **Le test du tutoriel officiel Kling e-commerce mode :** 3 vidéos test avant de produire en série. Si plusieurs vidéos ratent pour la même raison, on corrige la règle commune, pas chaque prompt.
9. **Pas de son Kling pour nous** : rien ne garantit le polonais. La voix et la musique seront ajoutées au montage, ce qui économise aussi des crédits.

### Côté Meta
1. **Les 3 premières secondes décident de tout.** Si moins de 25 % des gens regardent au-delà de 3 s, l'accroche est ratée. La même vidéo avec deux accroches différentes peut avoir des résultats qui varient de 40 à 60 %.
2. **Format 9:16, 6 à 15 secondes**, sous-titres incrustés : la plupart des gens regardent sans le son.
3. **Le style UGC** (filmé au téléphone, naturel) bat en général le style « pub léchée » pour trouver de nouveaux clients.
4. **Varier les concepts** : 3 à 6 créations vraiment différentes par ensemble de publicités (Meta recommande 6 avec Advantage+).
5. **Les pubs s'usent** : à renouveler quand la fréquence dépasse 3,5 en 7 jours ou que le coût par vente monte de 30 %. Les Reels s'usent environ 40 % plus vite.

### Côté légal (important pour vous)
- Meta autorise les pubs faites avec l'IA. **Une personne photoréaliste générée par IA** peut déclencher l'étiquette « Informations sur l'IA », automatiquement si le fichier contient des métadonnées IA, ou par une déclaration manuelle.
- **AI Act européen, article 50, en vigueur depuis le 2 août 2026** : les contenus réalistes générés par IA (deepfakes) doivent être signalés clairement.
- **Un avatar IA ne doit jamais se faire passer pour une vraie cliente.** C'est de la publicité trompeuse, même avec la mention IA. Nos scripts présentent le produit, ils ne témoignent pas.
- **Le collant montré doit être le vrai** : teinte taupe fumé, et non une peau nue parfaite. Sinon vous aurez des retours et des réclamations.

---

## 3. Le plan concret : budget pilote d'environ 120 crédits

### Étape 0 : gratuit, avant tout achat
- Envoyer les photos de référence à Kling. **C'est testé et ça fonctionne** (photo 10 envoyée).
- Créer l'**Element « Ciepelle – rajstopy »** :
  - photo principale : **10** (porté chair) ;
  - secondaires : **02** (doublure polaire), **08** (dos, couture), **06** (noir porté).

### Étape 1 : 4 images fixes (~8 crédits)
Modèle : **Kling Image 3.0 Omni**, format 9:16, 2K, 1 image par plan. Les prompts sont en anglais (meilleur rendu), avec les références et l'Element.

| # | Plan | Références | Prompt (résumé) |
|---|---|---|---|
| A | **Accroche** : arrêt de tram en décembre, jambes en robe | Element + 图片1 = photo 01 (ambiance rue) | Smartphone UGC shot, Polish city tram stop, frosty winter morning, overcast daylight, woman in camel coat and short knit dress wearing <<<collant>>>, framed waist down, black ankle boots, natural unpolished look |
| B | **La preuve** : doublure retournée | 图片1 = 02, 图片2 = 05 | Close-up from above, waistband folded down revealing thick golden-camel plush fleece lining, sheer smoky outer layer, warm lamp light, beige knit blanket, hand brushing the fleece |
| C | **Le pincement** : « ce n'est pas ma peau » | Element + 图片1 = 00 (geste) | Close-up on knee, fingers pinching and pulling the sheer fabric away from the leg, showing it is tights, cozy indoor light |
| D | **Les 3 couleurs** | 图片1 = 10, 图片2 = 06, 图片3 = 12 | Three pairs of legs lying on white bed sheets: nude-taupe, black, grey, same tights model, soft daylight, top-down |

**Contrôle avant d'aller plus loin**, en comparant à vos photos :
- teinte taupe fumé (pas une peau nue) ;
- polaire couleur caramel ;
- taille haute, couture au dos ;
- mains correctes ;
- aucun texte ni logo parasite.

**Je vous montre les 4 images. Vous validez ou non.** On ne régénère que ce qui rate, en corrigeant le prompt.

### Étape 2 : 3 vidéos test (~90 crédits)
Modèle : **Kling 3.0 Turbo** (image vers vidéo, une seule image), 5 s, 720p.

| Vidéo | Image de départ | Mouvement demandé |
|---|---|---|
| A | Arrêt de tram | Slow push-in, breath visible in cold air, subtle coat movement, legs stay still |
| B | Doublure | Static close-up, hand slowly strokes the fleece, fabric texture stays consistent |
| C | Pincement | Fingers pinch and gently release the fabric, it snaps back, no morphing |

On vérifie : le tissu ne se déforme pas, les mains sont naturelles, la teinte est stable. **Si une vidéo rate, on ne la relance pas telle quelle** : on corrige le prompt d'abord.

### Étape 3 : montage (gratuit, CapCut)
- Accroche texte dans la 1ʳᵉ seconde : « Grudzień. Sukienka. Gołe nogi? 🥶 »
- Voix off polonaise : synthèse vocale CapCut, ou HeyGen / Hedra pour un visage qui parle.
- Sous-titres, musique libre de droits, fin avec « Ciepelle · darmowa dostawa · 14 dni na zwrot ».
- Mention « contenu généré par IA » activée dans Meta.

### Étape 4 : passage à l'échelle
Avec les règles validées, chaque nouvelle pub coûte **~2 crédits par image + ~30 crédits par plan vidéo**. Une pub de 3 plans revient à **~100 crédits (~1,50 $ ≈ 6 zł)**. Avec 660 crédits (~42 zł / ~10 €) : **le pilote + environ 5 pubs complètes**.

---

## 4. Ce qu'il faut pour démarrer
- [ ] Recharger Kling. **Le Standard à ~10 $ suffit pour le pilote.**
- [ ] Me dire « go » : je crée l'Element, je génère les 4 images, je vous les montre et j'attends votre validation avant toute vidéo.

## Sources
- [Kling – guide officiel des prompts](https://kling.ai/blog/kling-ai-prompt-guide)
- [Kling – tutoriel MCP mode e-commerce](https://kling.ai/blog/claude-kling-mcp-fashion-video-workflow)
- [Atlabs – guide Kling 3.0](https://www.atlabs.ai/blog/kling-3-0-prompting-guide-master-ai-video-generation)
- [Shhots – coûts en crédits Kling 2026](https://shhots.ai/blog/kling-ai-pricing/)
- [Imagine.art – tarif Kling 3.0 Turbo](https://www.imagine.art/blogs/kling-3-0-turbo-pricing)
- [AdLibrary – bonnes pratiques créatives Meta 2026](https://adlibrary.com/posts/meta-ad-creative-best-practices)
- [Benly – vidéos Meta](https://benly.ai/learn/meta-ads/video-ads-guide)
- [Cinerads – obligations de mention IA (Meta, UE)](https://www.cinerads.com/blog/ai-ad-disclosure-requirements)
- [Cinerads – politique Meta sur l'UGC IA](https://www.cinerads.com/blog/ai-ugc-facebook-ad-policy)
