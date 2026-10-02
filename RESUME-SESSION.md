# Ciepelle : résumé de la session (pour reprendre dans une nouvelle conversation)

## Contexte
- Boutique Shopify **purrpeak.com** (myshopify `8wxxc1-gx`), marque **Ciepelle**. Dropshipping via DSers de **collants polaires effet peau nue**, vendus en **Pologne**.
- Gamme :
  - grammages 80 / 220 / 300 g ;
  - couleurs **Cielisty** (chair), **Czarny** (noir), **Szary** (gris, ajouté pendant la session) ;
  - lots de 1, 2 ou 3 paires.
- Prix réels (PLN) :

  | Grammage | 1 paire | 2 paires | 3 paires |
  |---|---|---|---|
  | 80 g | 79 zł | 119 zł | 149 zł |
  | 220 g | 99 zł | 149 zł (offre phare) | 189 zł |
  | 300 g | 119 zł | 179 zł | 229 zł |

- Règles de l'utilisateur :
  - parler en **français** ;
  - montants en **zł avec l'équivalent en €** ;
  - peu de captures d'écran ;
  - **pas d'allégation santé, pas de faux prix barrés** ;
  - **plus aucun budget pour des outils** : le reste de l'argent sert aux pubs Meta.

## Ce qui a été fait

### Boutique
- **Thèmes** :
  - v4 publié (émojis restaurés, gris ajouté dans les textes et la FAQ, pastille de couleur grise) ;
  - v5 préparé, **non publié** : texte de saison sans allusion santé.
- **Produit** : 27 variantes, dont 9 grises créées **à stock 0**. Le prix catalogue PLN est fixé via la liste de prix.

### DSers
- Mapping vérifié, correct pour chair et noir.
- **Gris non relié** au fournisseur (« Grey Pantyhose ×1/×2/×3 ») : à faire par l'utilisateur.
- Fournisseur de secours (Exquisite Underwear Store, AliExpress 1005006188489629) **pas encore ajouté**.

### Documents produits
- `ciepelle-business/business-plan-meta.md` :
  - marges : 40 à 71 zł par commande ;
  - objectif : coût par vente < 45 zł (≈ 10,6 €), ROAS > 3 ;
  - 3 scénarios ;
  - calendrier de saison.
- `ciepelle-business/plan-kling-meta.md` : méthode Kling et règles Meta / IA.
- `references-ciepelle/` : photos produit et fiche de prompts.

### Veille TrendTrack
Pubs concurrentes analysées :
- Feelwonder (DE)
- Collant Leggs (FR)
- Le Collant Frenchie (FR, 47,9 M de personnes atteintes)
- FleeceWereld (NL)
- Cose Online (IT)
- Veritas (BE)
- Magic Curve

On reprend leurs **structures**, jamais leurs vidéos. L'assistant a refusé de modifier la vidéo Frenchie (changer le visage, recolorer le collant) : contrefaçon, et visage d'une vraie personne.

## Les 2 pubs prêtes (format 9:16, textes en polonais, musique originale libre de droits)

### 1. Pub « défilé » : `kling-defile/pub-defile-ciepelle.mp4` (13,3 s, 150 BPM)
- **Image** : jambes seules en défilé (chair, noir, gris) dans une salle claire.
- **Textes** :
  - accroche « Wyglądają jak gołe nogi… » ;
  - plan polaire « …a w środku polar. » ;
  - noms des couleurs ;
  - sortie dans la neige « A za drzwiami… zima. ».
- **Son** : la musique s'éloigne, puis vent d'hiver.
- **Fin** : logo Ciepelle qui frappe au centre de l'image.
- Scripts : `kling-defile/montage/plan.py`, `montage.py`, `audio/music.py`.

### 2. Pub « essayage » : `kling-essayage/pub-essayage-ciepelle.mp4` (12,5 s)
Même structure et même minutage que la pub Frenchie, avec ses phrases traduites en polonais :

| Temps | Plan | Texte |
|---|---|---|
| 0–2,25 s | Femme en body, collant chair | « Wyglądają jak zwykłe przezroczyste rajstopy, ale… » |
| 2,25–4,5 s | Gros plan doux du polaire | « Ale… to ocieplane rajstopy z polarem na zimę » |
| 4,5–8,5 s | 4 tenues d'hiver | « Idealne, żeby nosić lekkie stylizacje tej zimy » |
| 8,5–10,5 s | 2 tenues | « Im więcej par, tym więcej oszczędzasz » (vrai : la paire revient à 99 / 74,50 / 63 zł) |
| fin | Logo + « Zestaw 3 par już od 149 zł » | — |

- 6 tenues avec la même femme : chair ×3, noir, gris ×2. Le visage est coupé sous le nez.
- Scripts : `kling-essayage/montage/plan.py`, `montage.py`, `audio/music.py`.

## Kling (génération IA)
- Connecté via MCP. **Solde : 1 crédit.**
- L'utilisateur ne veut plus payer. Si l'abonnement Standard est mensuel, il recharge environ 660 crédits à la date de renouvellement.
- **Demande en attente** : la même pub essayage avec **un joli visage bien visible**, identique dans tous les plans. Elle sert d'accroche ; la femme finit d'enfiler son collant au début.
  - Coût estimé : environ 230 crédits (portrait, puis personnage réutilisable, puis images et vidéos).
  - Impossible sans crédits : aucune solution gratuite de qualité sur la machine (pas de carte graphique).

## Prochaine étape : lancement Meta (en cours)
Plan donné à l'utilisateur :

1. **Avant de lancer** :
   - relier le **gris** dans DSers (ou retirer « szary » du texte de la pub) ;
   - corriger la page Contact (« Trade name: AquaFlow ») dans Shopify.
2. **Relier la boutique** : app Facebook & Instagram dans Shopify, pixel et API Conversions, partage des données sur « Maximum », achat test.
3. **Campagne** :
   - objectif **Ventes**, type **Advantage+** ;
   - Pologne, femmes 22–55 ans, placements automatiques ;
   - **80 zł/jour (≈ 19 €)** ;
   - les 2 vidéos dans la même campagne ;
   - **mention IA cochée**.
4. **Textes (PL)** :
   - Texte principal :
     > Wyglądają jak zwykłe cienkie rajstopy, a w środku mają miękki polar. Noś sukienki i spódnice nawet zimą ❄️
     > ✔ cielisty, czarny lub szary
     > ✔ 80 g, 220 g lub 300 g
     > Im więcej par, tym więcej oszczędzasz: 1 para 99 zł, 2 pary 149 zł, 3 pary 189 zł (220 g).
   - Titre : « Rajstopy z polarem – efekt gołych nóg »
   - Description : « Zestawy 2 i 3 par taniej »
   - Bouton : « Kup teraz »
5. **Règles de décision** :
   - couper une pub à 120 zł dépensés sans vente ;
   - coût par vente < 45 zł pendant 3 jours : +20 % de budget ;
   - coût par vente > 60 zł pendant 4 jours : couper ;
   - 560 zł (≈ 130 €) dépensés sans pub rentable : tout arrêter et revoir l'offre ;
   - ne rien toucher pendant les 3 premiers jours.
6. **Suivi** : envoyer tous les 2–3 jours une capture du Gestionnaire de publicités (dépense, CPM, CTR, achats, coût par achat).

**Question restée ouverte** : le gris, on le relie dans DSers ou on le retire du texte pour l'instant ?

## Autres tâches en attente côté utilisateur
- Publier le thème v5.
- Transmettre les **9 coûts fournisseur** (3 couleurs × 3 grammages) pour recalculer le business plan.
- Ajouter le fournisseur de secours dans DSers.
- Vérifier la TVA / le guichet unique (OSS) avec un comptable.

Dépôt Git : branche `claude/ciepelle-shopify-resume-vh7vey`. Tous les fichiers ci-dessus y sont enregistrés.
