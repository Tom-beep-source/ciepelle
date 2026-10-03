# Ciepelle : résumé pour la prochaine session (3 octobre 2026)

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

## DSers (vérifié après rechargement)
- **Produit principal** : 27 déclinaisons en mapping avancé vers **Stone's Store**, AliExpress 1005006966171723. Variantes « {g}-Coffee/Black Pantyhose1/Grey Pantyhose », quantité 1, 2 ou 3 selon le lot.
- **Trio** : mapping avancé vers **COZOK Gal Store**, AliExpress 1005007430201854.
  - Chaque grammage commande 3 articles : Coffee + Black + Grey Pantyhose « {g} L(40-70kg) », quantité 1 chacun.
  - COZOK annonce ~2 000 paires en stock par déclinaison mais n'a que 12 ventes : **commande test obligatoire**.
- **Fournisseur de secours non ajouté** : Exquisite Underwear Store, AliExpress 1005006188489629 (10 000+ ventes, tailles L, XL, 2XL).

## Thèmes
- **v7** est en ligne.
- **v8** (OnlineStoreTheme/200464597366) **est prête mais pas publiée**. Elle contient :
  - la correction typographique (« ? » non isolé, titres équilibrés : `assets/ciepelle-typo.css` + `ciepelle-typo.js`) ;
  - le paiement forcé en polonais : le panier envoie vers `/checkout?locale=pl`, et « Kup teraz » utilise `return_to=/checkout?locale=pl`.
  - **À tester avant publication** : le bouton « Przejdź do kasy » de l'aperçu v8 doit ouvrir le paiement en polonais. Mon dernier clic automatique n'a pas déclenché la navigation ; c'est probablement un raté de clic, à confirmer.
- **Accueil** : le lien « Jak wybrać grubość » mène au comparatif avec les photos de polaire (`snippets/weight-compare.liquid`), suivi d'un bandeau Trio (`snippets/trio-banner.liquid`).

## Corrigé pendant cet audit
- Anciennes traductions polonaises qui affichaient « PurrPeak » dans les Conditions de service et la Politique d'expédition : supprimées.
- Page Coordonnées : « AquaFlow » remplacé par Tom Canal EI / Ciepelle + SIRET.
- L'anglais (/en) est désactivé sur purrpeak.com. Avant, le panier redirigeait vers /en/cart et le paiement s'affichait en anglais.
- Vérifiés OK :
  - livraison gratuite en Pologne pour les 30 déclinaisons ;
  - BLIK et PayPal présents au paiement ;
  - aucun lien mort, aucune erreur Liquid ;
  - les 27 déclinaisons et les 3 Trio s'ajoutent au panier au bon prix en PLN.

## Reste à faire

### Audit (en cours)
1. Publier la v8 après le test du bouton « Przejdź do kasy ».
2. **Coûts fournisseurs réels et marges.** Relever les prix pour les 9 combinaisons couleur × grammage, chez Stone's Store et chez COZOK.
   - Méthode : sur la page AliExpress du produit, appeler `window.lib.mtop.request({api:'mtop.aliexpress.pdp.pc.query', v:'1.0', type:'GET', dataType:'jsonp', data:{productId, _lang:'en_US', _currency:'PLN', country:'PL', clientType:'pc', ext:'{}'}})`. Le résultat contient `SKU.skuPaths` (skuStock) et `PRICE.skuPriceInfoMap`.
   - Recalculer ensuite la marge des 27 déclinaisons et des 3 Trio, en tenant compte de la TVA, d'environ 3 % de frais et de 5 % de provision pour retours.
   - Mettre à jour `ciepelle-business/business-plan-meta.md`.
3. **Alertes de stock.** Dans DSers → Paramètres, activer la synchronisation automatique du stock et des prix, ainsi que les notifications de rupture et de changement de prix. Dans Shopify, prévoir une alerte de stock bas (l'app Flow est gratuite, si elle est disponible).
4. Ajouter Exquisite comme fournisseur de secours dans DSers.
5. Rédiger le rapport final de l'audit pour l'utilisateur.

### Côté utilisateur
- Shopify → Paramètres → Général : ajouter la ville **Muret** dans l'adresse de la boutique (la page Coordonnées affiche « 31600, Francja » sans ville).
- **Commande test** de bout en bout, de préférence un Trio : paiement, envoi DSers, délai réel jusqu'en Pologne.
- Faire valider la **TVA** par un comptable. Shopify ne collecte aucune TVA pour l'UE alors que le site indique « prix TTC » ; en micro-entreprise, il est peut-être en franchise de TVA.
- Passer le dépôt GitHub en **privé** : il est public.

### Ensuite : lancement Meta
- Expliquer simplement comment fonctionnent Meta et une campagne.
- Installer l'app Facebook & Instagram dans Shopify : pixel, API Conversions, partage des données sur « Maximum ».
- Campagne **Ventes Advantage+** : Pologne, femmes 22–55 ans, environ 80 zł/jour (≈ 19 €), mention IA cochée.
- Pubs prêtes :
  - `kling-essayage/pub-essayage-ciepelle.mp4` (logo en haut à gauche, version du 2 octobre) ;
  - `kling-defile/pub-defile-ciepelle.mp4`.
- Rédiger les textes de vente en polonais : variantes de texte principal, de titre et de description, plus une version Trio. Pas d'allégation santé, pas de faux prix barré.
- Règles de décision : voir `ciepelle-business/business-plan-meta.md`, § 6.D.
