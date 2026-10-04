# Ciepelle : résumé pour la prochaine session (mis à jour le 3 octobre 2026, fin de journée)

Parle à l'utilisateur en **français**. Affiche toujours les montants en **zł avec l'équivalent en €** (1 € ≈ 4,25 zł). Il est débutant : réponds sans jargon, en peu de mots, avec peu de captures d'écran. **Il n'a plus de budget pour des outils** : l'argent restant est réservé aux pubs Meta.

## Contexte
- Boutique Shopify **purrpeak.com** (admin : `aquaflow-boutique`, myshopify `8wxxc1-gx`), marque **Ciepelle**. Dropshipping via **DSers** de collants polaires effet jambes nues, vendus en **Pologne**.
- Le vendeur est **Tom Canal EI**, 68 Avenue des Pyrénées, 31600 Muret, SIRET 10762343100015, contact support@purrpeak.com.
- Les fichiers du thème sont dans ce dépôt, dossier `ciepelle-theme/`. Pour les envoyer : `themeFilesUpsert` avec `body: {type: URL, value: raw.githubusercontent.com/...<commit>/...}`.
- **On ne peut pas modifier le thème en ligne.** Il faut dupliquer le thème (`themeDuplicate`), modifier la copie, et c'est l'utilisateur qui la publie.

## Produits (vérifiés le 3 octobre)
- **Produit principal** `rajstopy-ocieplane-polarem-z-efektem-nagich-nog-220-g` (gid Product/15907398943094) : 27 déclinaisons, combinaisons de 3 options.
  - Option « Zestaw » : 1 para / 2 pary (najczęściej wybierane) / 3 pary.
  - Option « Kolor » : Cielisty (chair) / Czarny (noir) / Szary (gris).
  - Option « Gramatura » : 80 / 220 / 300 g.

  | Grammage | 1 paire | 2 paires | 3 paires |
  |---|---|---|---|
  | 80 g | 79 zł | 119 zł | 149 zł |
  | 220 g | 99 zł | 149 zł | 189 zł |
  | 300 g | 119 zł | 179 zł | 229 zł |

  Prix PLN fixés dans la liste de prix PriceList/38354846070. La photo grise est reliée aux 9 déclinaisons grises. La photo « 3 couleurs » est en 2ᵉ position de la galerie : réglages w80 / w220 / w300 dans `templates/product.json`.
- **Zestaw Trio** `zestaw-trio-rajstopy-z-polarem` (Product/15912900788598), modèle de page `product.trio` : une paire chair, une noire et une grise, au choix en 80 / 220 / 300 g.
  - Prix : 149 / 189 / 229 zł, en vente.
  - Première photo : les 3 couleurs côte à côte, image construite à partir des vraies photos.
- **Stock suivi**, vente bloquée en cas de rupture. Valeurs saisies le 3 octobre, en paires chez le fournisseur.
  - Fournisseur principal : chair 78 / 33 / 4 ; noir 346 / 58 / 41 ; gris 10 / 5 / 2568 (limité à 200).
  - Les lots sont divisés par 2 ou 3. Le Trio est à 300.
- Les anciens produits PurrPeak (arbres à chat) sont archivés.

## DSers (revérifié le 4 octobre après rechargement)
- **4 oct : chair 300 g, gris 80 g et gris 220 g (×1/2/3 paires, 9 déclinaisons) basculés sur COZOK** (Stone's n'avait plus que 2 / 9 / 5 paires ; COZOK ~2 000). Stock Shopify mis à jour. Synchro auto des stocks DSers = payante (19,9 $/mois), non activée. Livraison DSers par défaut : AliExpress Standard (suivi).
- **Produit principal** : 27 déclinaisons en mapping avancé vers **Stone's Store**, AliExpress 1005006966171723. Variantes « {g}-Coffee/Black Pantyhose1/Grey Pantyhose », quantité 1, 2 ou 3 selon le lot.
- **Trio** : mapping avancé vers **COZOK Gal Store**, AliExpress 1005007430201854.
  - Chaque grammage commande 3 articles : Coffee + Black + Grey Pantyhose « {g} L(40-70kg) », quantité 1 chacun.
  - COZOK annonce ~2 000 paires en stock par déclinaison mais n'a que 12 ventes : **commande test obligatoire**.
- **Fournisseur de secours non ajouté** : Exquisite Underwear Store, AliExpress 1005006188489629 (10 000+ ventes, tailles L, XL, 2XL).

## Thèmes
- **v7** est en ligne.
- **v8** (OnlineStoreTheme/200464597366) **est prête et testée, mais pas publiée.** Elle contient :
  - la correction typographique ;
  - le paiement forcé en polonais.

  Le 3 octobre, testé avec Chromium (navigateur réglé en anglais) : « Przejdź do kasy » et « Kup teraz » ouvrent le paiement **en polonais, en PLN**.
  - **L'utilisateur doit publier la v8** lui-même.
  - Point connu, laissé tel quel : « Kup teraz » ajoute l'article au panier existant. L'autre méthode testée (lien panier direct) remplace le panier, ce qui est pire.
- Le 3 octobre, la description SEO du produit principal a été corrigée : elle cite maintenant « cielisty, czarny i szary ».

## Ce qui a été fait le 3 octobre
- **Marges** : `ciepelle-business/marges.py` et `couts-fournisseurs.json` produisent `marges.md` (27 déclinaisons + 3 Trio, avec TVA 23 % et sans TVA). Le business plan a été mis à jour, Trio compris.
  - ⚠️ **Les coûts sont encore estimés** (80 g = 3,81 $ ; 220 g ≈ 5,80 $ ; 300 g ≈ 7,84 $ ; livraison 0,99 $ par paire).
  - AliExpress bloque le navigateur automatique (vérification anti-robot, à ne pas contourner). Shopify ne contient aucun coût. Aucun outil DSers n'est disponible dans les sessions cloud.
  - **Il faut que l'utilisateur donne les 12 prix DSers** : Stone's Store 9 (couleur × grammage) + COZOK 3 (un Trio par grammage). Ensuite : `python3 marges.py`.
- **Rapport d'audit + textes Meta** : `RAPPORT-AUDIT-ET-META.md`.
  - Contient : fonctionnement de Meta, installation du pixel, réglages de campagne, textes polonais pour le Défilé, l'Essayage et le Trio.
- **Page Facebook « Ciepelle »** : créée par l'utilisateur, https://www.facebook.com/profile.php?id=61594721714264.
  - Page vérifiée sur capture : couverture, nom et bio polonaise OK.
  - Encore à faire : remplacer la photo de profil par la version empilée (`meta-page/photo-profil.png`), ajouter la catégorie « Marque de vêtements », choisir le nom d'utilisateur @ciepelle.pl, publier les posts.
  - **Ne pas mettre de site web** sur la page tant que le domaine final n'est pas choisi.
  - L'ancienne page « AutoRec », de 3 ans, était restreinte. On ne l'utilise pas et on ne la renomme pas. Elle est à retirer du portefeuille business.
- **Kit page Meta** : `meta-page/`. Il contient :
  - `KIT-PAGE-META.md` : analyse TrendTrack des pages concurrentes, bio, « À propos », réponses automatiques, légendes polonaises, hashtags ;
  - `couverture-facebook.png`, `photo-profil.png` ;
  - `posts/` : 6 premiers posts (4 visuels 4:5 + 2 vidéos).
  - Ce que montre l'analyse : les gagnants ont de petites pages (Feelwonder 415 mentions J'aime → 10,9 M de personnes touchées). Le concurrent polonais Polarove (polarove.pl) a eu ses pubs arrêtées au bout de 3 jours, avec une page vide et des promesses « −10 °C » et « 1+1 gratis ».
- **5 variantes de pub** : `kling-variantes/sortie/ciepelle-variante-A…E.mp4`, toutes en polonais, de 6 à 12 s.
  - A « Sukienka zimą i nie marzniesz? »
  - B « Jeden model. Trzy kolory. »
  - C « POV: wszyscy myślą, że masz gołe nogi »
  - D « Za oknem zima… »
  - E version courte
  - Rendu : `./rendre.sh X` (structures dans `variantes.py`).
  - Guide TikTok : `kling-variantes/TIKTOK.md`. L'utilisateur va les publier gratuitement sur un **compte pro TikTok @ciepelle.pl**. La variante qui fait le plus de vues deviendra la première pub Meta.
  - Avec les 2 pubs déjà prêtes (`kling-defile/pub-defile-ciepelle.mp4` et `kling-essayage/pub-essayage-ciepelle.mp4`), on a 7 vidéos au total.
- **Domaine** : purrpeak.com, acheté chez IONOS, n'est pas cohérent avec la marque.
  - Disponibles : **ciepelle.pl** (18 $ ≈ 66 zł / 15,5 €, recommandé), ciepelle.com (16 $), ciepelle.store (9 $).
  - L'utilisateur demande à IONOS un remboursement ou un échange (garantie 30 jours ?).
  - **Décision : attendre le domaine final avant de le renseigner dans Meta** (page, pixel, vérification du domaine), pour éviter les changements suspects.
- **Adresse légale** : l'utilisateur hésitait à mettre son adresse française. Expliqué que c'est **obligatoire** (droit UE et polonais, UOKiK) : elle n'apparaît que dans les pages légales.
  - Proposition : ajouter sur la page Kontakt « Sklep Ciepelle prowadzony jest przez firmę z Unii Europejskiej… ». **À faire** (copie du thème) si l'utilisateur confirme.
- **Connecteur Meta pour Claude** : pas de connecteur officiel. Windsor.ai (formule gratuite à vérifier) ou, gratuit, export CSV du Gestionnaire de publicités à envoyer à Claude. TrendTrack peut suivre ses propres pubs une fois en ligne (portée, durée), mais pas les ventes.
- **Kling** : il reste 1 crédit. Une version de la pub essayage avec un **visage visible** est demandée : environ 230 crédits, à faire seulement si les crédits mensuels sont rechargés. L'utilisateur ne veut plus rien payer.

## En attente de la paye de l'utilisateur (budget pubs)
1. Domaine final, relié à Shopify et défini comme domaine principal (redirection automatique de purrpeak.com).
2. App Facebook & Instagram dans Shopify : pixel, partage des données sur « Maximum », vérification du domaine dans Meta.
3. Campagne **Ventes Advantage+** :
   - Pologne, femmes 22–55 ans, **80 zł/jour (≈ 19 €)**, mention IA ;
   - les 3 vidéos les plus vues sur TikTok ;
   - limite de dépense du compte : 150 € ;
   - règles de décision dans `ciepelle-business/business-plan-meta.md` § 6.D (coupe à 120 zł sans vente ; +20 % si coût par vente < 45 zł ; arrêt à 560 zł sans pub rentable).
4. Compte publicitaire : devise **EUR**, fuseau **Europe/Warsaw**. L'utilisateur doit envoyer une capture de « Paramètres → Comptes publicitaires » pour vérification.

## Reste à faire côté utilisateur (gratuit)
- Publier la v8.
- Finir la page Facebook, puis publier 1 à 2 posts par jour.
- Ouvrir le compte TikTok pro et publier 1 variante par jour (18 h–21 h, heure de Varsovie).
- Envoyer les 12 prix DSers.
- Dans DSers : synchronisation stock/prix et notifications. Dans Shopify : app Flow, alerte de stock bas (seuil 5).
- Ajouter Exquisite (AliExpress 1005006188489629) comme fournisseur de secours dans DSers. **Urgent** : il reste 4 paires de chair 300 g et 5 paires de gris 220 g chez Stone's Store.
- Adresse complète de la boutique dans Shopify → Paramètres → Général (Tom Canal EI, Muret, Francja).
- Commande test, de préférence un Trio.
- Faire valider la TVA par un comptable.
- Passer le dépôt GitHub en privé.
- Proposé, gratuit : app « Google & YouTube » dans Shopify, pour des fiches gratuites dans Google Shopping.
