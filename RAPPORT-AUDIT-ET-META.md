# Ciepelle : rapport d'audit et lancement Meta (3 octobre 2026)

## 1. Rapport d'audit

### Testé et corrigé aujourd'hui
- **Paiement en polonais (aperçu v8) : OK.**
  - Testé avec un vrai navigateur, réglé en anglais.
  - « Przejdź do kasy » ouvre le paiement en polonais, en złotys.
  - « Kup teraz » aussi.
- **Description Google du produit** : elle oubliait le gris. Elle dit maintenant « Kolory: cielisty, czarny i szary ».
- **Calcul automatique des marges** : il couvre les 27 déclinaisons et les 3 Trio, avec et sans TVA. Fichiers : `ciepelle-business/marges.py` et `couts-fournisseurs.json`. Le business plan est mis à jour, Trio compris.

### Point connu, non corrigé (sans gravité)
- « Kup teraz » ajoute l'article au panier existant. Si le client avait déjà autre chose dans son panier, il paie les deux. C'est le fonctionnement normal de ce type de bouton.
- L'autre méthode, testée aussi, remplace le panier, ce qui est pire. On garde donc la version actuelle.

### Bloqué de mon côté : à faire par toi
Je n'ai accès ni à DSers ni à ton Chrome dans cette session, et AliExpress bloque mon navigateur (vérification anti-robot).

1. **Publier la v8** : Shopify → Boutique en ligne → Thèmes → v8 → « Publier ».
2. **Relever les 12 coûts d'achat dans DSers** (Mes produits → le produit → Mapping, colonne coût) :
   - Stone's Store : chair, noir et gris × 80 / 220 / 300 g ;
   - COZOK : les mêmes 9, pour le Trio ;
   - avec le prix de livraison vers la Pologne.

   Envoie-les-moi en message : je mets à jour les marges en 1 minute. **Les marges actuelles reposent encore sur des estimations.**
3. **Alertes de stock** :
   - DSers → Paramètres → Synchronisation : activer la mise à jour automatique du stock et du prix.
   - DSers → Paramètres → Notifications : activer « Produit en rupture » et « Changement de prix ».
   - Shopify : installer l'app gratuite **Shopify Flow**, puis choisir le modèle « Recevoir une alerte de stock bas » avec un seuil de 5.
4. **Fournisseur de secours** :
   - DSers → le produit → Mapping → « Ajouter un fournisseur secondaire » ;
   - coller le lien `https://www.aliexpress.com/item/1005006188489629.html` ;
   - relier chaque déclinaison (couleur + grammage).
5. **Stocks faibles chez Stone's Store** : chair 300 g (4 paires), gris 220 g (5 paires), gris 80 g (10 paires). Dès qu'il y a des ventes, ces déclinaisons passeront en rupture : c'est pour ça que le fournisseur de secours est important.
6. Toujours en attente :
   - ajouter la ville « Muret » dans l'adresse de la boutique ;
   - passer une commande test (de préférence un Trio) ;
   - faire valider la TVA par un comptable ;
   - passer le dépôt GitHub en privé.

---

## 2. Meta, simplement

### Comment ça marche
- Tu donnes un budget par jour à Meta. Meta montre tes vidéos aux personnes les plus susceptibles d'acheter.
- Pour savoir qui achète, Meta a besoin d'un **pixel** : un petit mouchard installé sur ta boutique, qui lui dit « cette personne a acheté ». Plus il voit d'achats, mieux il cible.
- Les 3 premiers jours, Meta teste et apprend. **Il ne faut toucher à rien.**

### Installer le pixel (gratuit, 10 minutes)
1. Shopify → Applications → installer **Facebook & Instagram** (l'app officielle de Meta).
2. Se connecter avec ton compte Facebook, puis choisir ta page, ton compte publicitaire et créer ou choisir un **pixel**.
3. Partage des données : choisir **« Maximum »**. Ça active aussi l'API Conversions, qui récupère les achats même quand le navigateur bloque le pixel.
4. Pour vérifier : dans le Gestionnaire d'événements Meta, l'événement « Purchase » doit apparaître après une commande test.

### Paramétrer la campagne
| Réglage | Valeur |
|---|---|
| Objectif | **Ventes** |
| Type | **Advantage+ campagne de ventes** |
| Pays | Pologne |
| Public | Femmes, 22–55 ans (Meta élargit tout seul si besoin) |
| Placements | Automatiques |
| Budget | **80 zł/jour (≈ 19 €)** pour la campagne entière |
| Pubs | Défilé, essayage et Trio dans la même campagne |
| Mention IA | **À cocher** sur chaque pub (« Contenu généré par IA ») |

**Règles de décision :**
- Une pub dépense 120 zł (≈ 28 €) sans aucune vente : on la coupe.
- Coût par vente sous 45 zł (≈ 10,6 €) pendant 3 jours : +20 % de budget.
- Coût par vente au-dessus de 60 zł (≈ 14 €) pendant 4 jours : on coupe.
- 560 zł (≈ 130 €) dépensés sans aucune pub rentable : on arrête tout et on revoit l'offre.

---

## 3. Textes de vente en polonais (prêts à coller)

Les prix et la livraison gratuite sont vérifiés dans la boutique. Pas d'allégation santé, pas de faux prix barré.

### Pub 1 : Défilé (`kling-defile/pub-defile-ciepelle.mp4`)
- **Texte principal :**
  > Wyglądają jak gołe nogi… a w środku mają miękki polar ❄️
  > Rajstopy Ciepelle: z zewnątrz cienkie, w środku ciepłe.
  > ✔ 3 kolory: cielisty, czarny, szary
  > ✔ 3 grubości: 80, 220 lub 300 g
  > Darmowa dostawa w całej Polsce · 14 dni na zwrot
- **Titre :** Wyglądają jak gołe nogi. Grzeją jak polar.
- **Description :** Darmowa dostawa · 14 dni na zwrot
- **Bouton :** Kup teraz

### Pub 2 : Essayage (`kling-essayage/pub-essayage-ciepelle.mp4`)
- **Texte principal :**
  > Wyglądają jak zwykłe przezroczyste rajstopy… ale w środku mają polar 👗❄️
  > Noś sukienki i spódnice nawet zimą.
  > Im więcej par, tym więcej oszczędzasz:
  > 1 para 99 zł · 2 pary 149 zł · 3 pary 189 zł (220 g)
  > Darmowa dostawa w całej Polsce.
- **Titre :** Lekkie stylizacje nawet zimą
- **Description :** 2 pary za 149 zł · darmowa dostawa
- **Bouton :** Kup teraz

### Pub 3 : Zestaw Trio (vidéo essayage, ou photo « 3 couleurs », lien vers la page Trio)
- **Texte principal :**
  > Nie możesz się zdecydować? Weź wszystkie trzy 🤍🖤🩶
  > Zestaw Trio: cielisty, czarny i szary – rajstopy z polarem, które z zewnątrz wyglądają jak cienkie rajstopy.
  > 3 pary: 149 zł (80 g) · 189 zł (220 g) · 229 zł (300 g)
  > Darmowa dostawa w całej Polsce.
- **Titre :** Zestaw Trio – 3 kolory od 149 zł
- **Description :** Cielisty + czarny + szary
- **Bouton :** Kup teraz
- **Lien :** https://purrpeak.com/products/zestaw-trio-rajstopy-z-polarem
