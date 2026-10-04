# Ciepelle : résumé de la session du 4 octobre 2026 (suite)

À lire avec `RESUME-SESSION.md` et `BILAN-3-4-OCTOBRE.md`.
Taux de change à utiliser désormais : **1 € = 4,37 zł** (taux officiel de la banque de Pologne au 2 octobre 2026). L'ancien taux de 4,25 était trop bas : les montants en € des anciens fichiers sont surestimés d'environ 3 %.

**Où est le travail :** branche GitHub **`claude/cool-darwin-gk448j`**. Elle contient tout le travail de `claude/ciepelle-shopify-resume-vh7vey`, plus 3 ajouts : le graphique de rentabilité, les textes de pub corrigés et ce résumé. La branche `claude/ciepelle-shopify-resume-vh7vey` n'a **pas** encore ces ajouts : il faut les y fusionner.

---

## 1. Accès vérifiés en début de session
- **Meta (lecture seule) : OK.**
  - Compte « Ciepelle PL », en EUR, fuseau Europe/Warsaw, actif, 0 € dépensé.
  - La clé d'accès n'a que le droit de lire (`ads_read`) et expire le **2 décembre 2026**.
- **Shopify : OK.**
- **TrendTrack : OK.** Abonnement Professional, ≈ 9 500 crédits restants jusqu'au 30 octobre.

## 2. Analyse des prix et de la concurrence (TrendTrack + web)
**Prix d'une paire chez les concurrents polonais :**

| Vendeur | Prix |
|---|---|
| Allegro, vendeurs chinois sans marque | 29 à 45 zł |
| Superzebra | 64 zł, avec « 1 achetée = 1 offerte » |
| Gabriella Second Skin | 65,90 zł |
| Leggzie | 89 zł |
| vivozebra | 99 zł |
| Calzedonia (collants thermiques) | 80 à 110 zł |
| Polarove | 149,99 zł |

**Conclusion : ne pas toucher aux prix.**
- Les lots sont dans la moyenne du marché.
- La paire seule est un peu chère, mais elle sert surtout à rendre le lot de 2 intéressant.
- Baisser les prix est impossible avec les marges actuelles.
- Les monter est impossible sans avis clients et sans livraison rapide.

**Le vrai point faible de Ciepelle, c'est la livraison, pas le prix.** Les concurrents livrent en 1 à 2 jours avec paiement à la livraison ; Ciepelle livre en 7 à 12 jours.

**Concurrents actifs sur Meta en Pologne :**
- **Azja Sklep : le leader.**
  - 111 pubs en ligne, dont une qui tourne depuis 345 jours.
  - Nouvelles pubs relancées le 25 septembre 2026.
  - Toute la boutique fait environ 68 500 zł par mois.
  - Ses arguments : « jusqu'à −30 °C », paiement à la livraison.
- **Superzebra** : nouvelle pub en forte hausse depuis le 17 septembre.
- **Leggzie**, **Gabriella**, **Calzedonia** (grosse campagne de 9 jours en novembre 2025).

Tous promettent des températures et un effet minceur. **On ne copie pas** : c'est ce qui a fait couper les pubs de Polarove.

**Marché :**
- Femmes de 22 à 55 ans sur Meta en Pologne : environ 6 à 7 millions. Clientes réalistes : environ 1 à 1,5 million (estimation).
- Le frein n'est pas la taille du marché, c'est le budget.
- Les plus grosses pubs du secteur tournent de mi-novembre à janvier.

## 3. Rentabilité par commande (graphique)
**Fichiers :** `ciepelle-business/rentabilite-par-commande.png` (le graphique) et `rentabilite.py` (le script qui le produit).

**Une commande moyenne :**
- **Prix payé : 145 zł (33,3 €).**
- À retirer :
  - achat du produit + livraison AliExpress : 57 zł ;
  - TVA polonaise 23 % : 27 zł ;
  - frais de paiement (3 %) + réserve pour les retours (5 %) : 12 zł.
- **Il reste 49 zł (11,3 €) avant la pub.**

**Point mort :** une vente doit coûter **moins de 49 zł de pub**. Au-delà, chaque vente fait perdre de l'argent.

| Coût de la pub pour 1 vente | Gain par commande | Rentable sur le mois dès… |
|---|---|---|
| 30 zł, avec une bonne vidéo | +19 zł | 8 ventes |
| 40 zł, l'objectif | +9 zł | 16 ventes |
| 70 zł, la moyenne estimée du secteur de la mode en Pologne | −21 zł | jamais |

Frais fixes comptés : environ 148 zł (34 €) par mois pour Shopify Basic et le domaine.

**Frais à vérifier :** les clientes paient en zł et Shopify verse en euros. Les frais de conversion s'ajoutent, donc les frais de paiement réels sont plutôt de **4 à 5 %**, pas 3 %.

**Estimation pour le test de 150 € (≈ 656 zł, soit environ 8 jours à 80 zł/jour) :**
- première vente probable entre le jour 1 et le jour 3 ;
- en scénario moyen, environ 7 commandes et une perte d'environ 255 zł (≈ 58 €) ;
- rentable seulement si une vidéo descend sous 49 zł par vente : rentable au jour le jour dès la 2ᵉ semaine, test remboursé vers les jours 20 à 30 ;
- environ 1 chance sur 3 que ça marche du premier coup.

## 4. Pubs : on mise sur le lot de 2 (`RAPPORT-AUDIT-ET-META.md` mis à jour)

**Marge par offre, avant pub :**

| Offre | Marge |
|---|---|
| 1 paire | 32 à 45 zł (trop faible) |
| **2 paires 220 g** | **54 à 59 zł** |
| 3 paires 80 g | 54 à 69 zł |
| Trio 220 g | 41 zł (trop faible) |
| Trio 300 g | 36 zł (trop faible) |

**Changements dans le rapport :**
- **L'ancienne pub 3 « Trio » est remplacée par une pub « 2 pary ».**
  - Texte : « Jedna para na całą zimę? To za mało 😉 … 2 pary za 149 zł (220 g) – oszczędzasz 49 zł względem dwóch pojedynczych par. »
  - Elle mène au produit principal, où le lot de 2 est déjà sélectionné.
  - Le Trio reste en vente sur le site, mais on ne paie plus de pub pour lui.
- **Pub Défilé :** ajout de « 2 pary za 149 zł ».
- **Les 7 vidéos ne changent pas.** Leur fin, « Zestaw 3 par już od 149 zł », correspond au lot de 3 × 80 g, qui a une bonne marge. Et 149 zł est aussi le prix du lot de 2 × 220 g.

**Nouvelles règles de décision :**
- couper une pub à **100 zł** dépensés sans vente ;
- **+20 % de budget** seulement si une vente coûte **moins de 40 zł** ;
- **couper** une pub si une vente coûte **plus de 50 zł** pendant 4 jours ;
- **tout arrêter** à 560 zł dépensés sans pub rentable.

**À faire :** reporter ces règles dans `ciepelle-business/business-plan-meta.md` (pas encore fait).

## 5. Le circuit d'une commande, expliqué à Tom
1. La cliente paie sur le site. Shopify verse l'argent sur le compte de Tom **tous les jours**, avec environ 2 à 3 jours ouvrés de décalage.
2. DSers récupère la commande tout seul.
3. **Tom doit lui-même cliquer** dans DSers (Orders → Awaiting order → « Place order to AliExpress »), puis **payer AliExpress avec sa propre carte**. Le fournisseur n'est jamais payé automatiquement sur l'argent de la cliente.
4. Le fournisseur expédie directement chez la cliente.
5. DSers envoie le numéro de suivi à Shopify, et la cliente reçoit l'e-mail de suivi.

⚠️ **Tom avance l'argent du fournisseur avant d'être payé.** Il doit garder environ 300 à 500 zł (70 à 115 €) disponibles sur sa carte, en plus du budget pub.

## 6. Réglages vérifiés ou faits avec Tom (captures à l'appui)

**Shopify :**
- Téléphone obligatoire au paiement ✅
- Paiement par e-mail ✅, prénom et nom obligatoires ✅
- Shopify Payments actif ✅, versements **quotidiens** sur son compte CIC, en EUR ✅
- Mode test désactivé ✅
- Nom sur le relevé bancaire des clientes : « SP Ciepelle » ✅. Le téléphone d'assistance est obligatoire chez Shopify, donc son numéro perso est resté.
- Moyens de paiement : **BLIK actif** ✅, Visa, Mastercard, Apple Pay, Shop Pay, PayPal. Klarna désactivé, volontairement.
- **App CJdropshipping désinstallée** ✅ (vérifié par l'API)
- **Zone de livraison États-Unis supprimée** ✅ : il ne reste que la Pologne, « Darmowa dostawa (7–12 dni roboczych) ».
- **Thème v8 publié** ✅ : « Ciepelle PL v8 » est en ligne.
  - Vérifié sur le site public : tout est en polonais, prix en zł, « Kup teraz » présent, livraison et délai affichés, logos de paiement dont BLIK en bas de page.
  - Les mentions légales affichent « Tom Canal EI, Muret, Francja, SIRET ». « AquaFlow » a disparu.

**DSers :**
- Le compte DSers est relié à **3 boutiques**. Ciepelle s'appelle **8wxxc1-gx**. Les 3 ont les mêmes réglages.
- Numéro de suivi envoyé à Shopify dès sa réception ✅
- E-mail d'expédition Shopify envoyé à la cliente sans délai, plus un e-mail si le numéro change ✅
- Transporteur « Other » avec lien de suivi Cainiao ✅
- Mise à jour automatique du suivi : **7 jours**. L'option 14 jours est **payante** (19,9 $/mois), donc **refusée**.
- **Message par défaut au fournisseur enregistré** ✅ : « Please do not include any invoice, receipt or price in the package. This is a gift. Thank you! »
- Synchro des notes de commande : désactivée, volontairement. IOSS : laissé vide.

**Compte bancaire :** les versements arrivent sur le **compte personnel** de Tom. C'est légal en micro-entreprise tant que le chiffre d'affaires reste sous 10 000 € deux années de suite. **Tom ouvrira un compte séparé gratuit après les 10 premières ventes.**

## 7. Commande test
- **Tom ne peut pas faire de vraie commande test.**
- Solution proposée, gratuite : une commande en **mode test Shopify Payments**, avec la carte 4242 4242 4242 4242.
  - Elle vérifie le site, l'e-mail en polonais, l'arrivée de la commande dans Shopify et dans DSers.
  - Il **ne faut pas** cliquer sur « Place order » dans DSers, et il faut **désactiver le mode test ensuite**.
  - **Pas encore faite.**
- **La première vraie commande servira de test pour l'expédition.** Il faut la traiter pas à pas avec Tom, et garder un petit budget pub tant qu'elle n'est pas partie avec son numéro de suivi.

## 8. Point d'attention : stock de l'offre phare
- **2 paires chair 220 g : seulement 16 lots en stock** (Stone's Store, environ 33 paires). Avec 2 à 3 ventes par jour, épuisé en moins d'une semaine.
- **Solution :** basculer ces déclinaisons sur **COZOK** dans DSers (environ 2 000 paires), comme pour le chair 300 g et le gris le 4 octobre.
  - Contrepartie : 32 zł la paire au lieu de 25 zł, donc une marge du lot de 2 d'environ **45 zł** au lieu de 59 zł.
  - Conseil : basculer quand il reste environ 5 lots.
  - **Décision de Tom en attente.**

## 9. Prochaines étapes (gratuites)
1. Décider de la bascule chair 220 g vers COZOK (§ 8).
2. Commande en mode test (§ 7), si Tom le souhaite.
3. Finir la page Facebook :
   - photo de profil empilée ;
   - catégorie « Marque de vêtements » ;
   - nom d'utilisateur @ciepelle.pl ;
   - publier les 6 posts.
4. Ouvrir le compte TikTok pro @ciepelle.pl : 1 vidéo par jour entre 18 h et 21 h (heure de Varsovie).
5. Passer le dépôt GitHub en **privé**.
6. Ajouter le fournisseur de secours Exquisite (AliExpress 1005006188489629) dans DSers.
7. Faire valider la TVA par un comptable, et demander pour le compte bancaire séparé.
8. Reporter les nouvelles règles et le taux de 4,37 zł dans `business-plan-meta.md`, `RESUME-SESSION.md` et `couts-fournisseurs.json` (le champ `eur_pln`).

**Le jour de la paye :** domaine final, pixel Meta, carte et limite de 150 € sur Ciepelle PL, puis campagne Advantage+ à 80 zł/jour (≈ 18,3 €) avec les pubs Défilé, Essayage et « 2 pary ».
