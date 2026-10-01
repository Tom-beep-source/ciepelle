# Sortir un nouveau site à partir de ce template

Checklist pas à pas pour dupliquer ce dépôt pour un nouveau commerce. Voir
`CLAUDE.md` § *Réutilisable vs propre au client* pour la convention complète :
en résumé, **tout ce qui identifie le commerce vit dans `src/config.ts` et
`public/images/`** ; le reste du code ne devrait jamais bouger.

**Règle fixe : un client = un dépôt GitHub = un projet Cloudflare = un
domaine.** Jamais mélangés — ni deux clients dans un même dépôt, ni un dépôt
qui sert deux projets Cloudflare, ni un domaine partagé entre deux sites.

## 1. Créer le dépôt du nouveau client

**Via « Use this template » sur GitHub, jamais `git clone`.**

1. Sur le dépôt template (`template-vitrine`, ou celui-ci une fois généralisé),
   vérifier que **Settings → Template repository** est coché.
2. Bouton **Use this template → Create a new repository**, choisir le nom du
   nouveau dépôt (un par client, voir la règle en tête de fichier).
3. Cloner ce **nouveau** dépôt localement, puis installer :

```bash
git clone <nouveau dépôt> nom-du-nouveau-client
cd nom-du-nouveau-client
npm install
```

**Pourquoi pas `git clone` du dépôt template directement :** cloner le
template traîne tout son historique — chaque commit du client précédent,
avec ses données (nom, adresse, téléphone...) en clair dans les diffs. La
recherche du §7 vérifie l'état actuel des fichiers, **pas l'historique
git** : un `git clone` classique livre donc un nouveau dépôt dont l'historique
expose encore les données de tous les clients précédents, sans qu'aucune
vérification de cette checklist ne le détecte. « Use this template » part
d'un historique neuf (un seul commit initial), donc rien à fuiter.

**`core.hooksPath` ne se clone pas avec le dépôt** — c'est un réglage git
local, à relancer à chaque nouveau clone :

```bash
git config core.hooksPath .githooks
```

Sans ça, les contrôles qualité (contraste, axe-core, Lighthouse) ne tournent
pas avant les commits.

## 2. Identité de déploiement

Deux fichiers portent un identifiant propre au client, **en dehors de
`config.ts`** :

- `wrangler.jsonc` — champ `"name"` : identifiant du déploiement Cloudflare.
  Doit être unique par client (ex. `"template-vitrine"` → `"nom-du-nouveau-client"`).
- `astro.config.mjs` — champ `site` : domaine réel du client (ex.
  `"https://exemple.workers.dev"` → `"https://www.nouveau-client.fr"`). Sert au
  canonical, à l'URL de l'image OG et au JSON-LD ; laissé en placeholder tant
  que le domaine n'est pas connu casse ces trois éléments silencieusement.

**Avant l'achat du domaine (avant signature du client) :** mettre dans
`astro.config.mjs` l'URL provisoire fournie par Cloudflare
(`https://<name-de-wrangler.jsonc>.<compte>.workers.dev`) — c'est la seule
URL qui existe tant que le domaine définitif n'est pas acheté. Une fois le
client signé et le domaine acheté, remplacer `site` par le vrai domaine et
repousser (`git push` + redéploiement, voir §8) : canonical, image OG et
JSON-LD doivent pointer sur l'URL finale avant livraison, jamais sur le
`workers.dev` provisoire.

## 3. `src/config.ts` — tout le reste

Remplacer chaque champ. Ne jamais inventer une donnée réelle (téléphone,
email, horaires, avis) : si une information manque, mettre
`// À CONFIRMER avec le commerçant` plutôt qu'une valeur plausible (voir
CLAUDE.md § *Données client*).

- `business` : nom, tagline, description, type, price range, cuisine
  - `type` (`BusinessType`, `src/config.ts`) détermine le libellé de la
    section produits (`getMenuSectionLabels()`, utilisé par `Header.astro` et
    `Hero.astro`) et le `@type` du JSON-LD (`BUSINESS_SCHEMA_TYPE` dans
    `src/lib/jsonld.ts`). Valeurs disponibles : `"bakery"` (Bakery),
    `"restaurant"` (Restaurant), `"florist"` (Florist). Ajouter un nouveau
    métier demande une entrée dans les deux endroits ci-dessus.
  - `cuisine` : optionnel, propriété schema.org `servesCuisine` propre aux
    commerces alimentaires — laisser absent pour un métier non alimentaire
    (ex. fleuriste), elle n'est alors simplement pas émise dans le JSON-LD.
- `theme.colors` : palette relevée sur la devanture réelle du nouveau commerce
- `theme.fonts` : `heading`/`body` (noms) **et** `preconnect`/`stylesheets`
  (URLs des feuilles de police) si les polices changent — les trois vont
  ensemble, changer seulement les noms ne change rien au rendu
- `contact`, `hours`, `hoursHighlight`
- `media`, `menu[].image`, `gallery[]` : chemins vers les nouvelles photos
- `menu[].items[].price` : **le template ne fournit aucun prix par défaut**
  (`price` est optionnel, absent tant qu'il n'a pas été communiqué — `Menu.astro`
  n'affiche rien quand il manque). Ne jamais inventer un prix ni reprendre
  celui d'un concurrent, surtout sur une V1 de démarchage montrée avant
  signature : demander les vrais prix au commerçant, ou laisser le champ
  absent en attendant.
- `menu[].items[].ingredients`, `allergenes`, `details` : voir §4 bis
- `infoPage` : voir §4 bis
- `commandes` : section optionnelle, voir §4 ter — à supprimer entièrement
  (`undefined`) si le commerce ne prend pas de commandes à l'avance
- `testimonials` : vrais avis autorisés, ou avis `// FICTIF` sans note chiffrée
- `practical`, `structured`, `social`
- `map` : voir §5
- `forms.web3formsAccessKey` : créer une nouvelle clé
  [web3forms.com](https://web3forms.com) pour ce client — **ne pas réutiliser
  celle d'un client précédent**, ses messages arriveraient sur le mauvais compte.
  Réutilisée telle quelle par le formulaire de la section Commandes (§4 ter)
  s'il est activé : une seule clé pour tout le site.
- `seo`

## 4. Photos

**Tant que les vraies photos ne sont pas fournies**, ne jamais utiliser de
banque d'images (Unsplash ou autre) : voir CLAUDE.md § *Photos* — le risque
d'enseigne ou de prix d'un autre commerce visible est trop élevé.
Utiliser à la place des aplats générés dans la palette du client :

```bash
npm run placeholders   # écrase les fichiers de public/images/ listés dans config.ts
```

`scripts/generate-placeholder-images.mjs` lit `theme.colors`, `business.name`
et `contact.address.city` dans `config.ts` et régénère logo, hero, à propos,
galerie, vignettes produits et image OG — le logo est un monogramme (initiales
du commerce sur la couleur `primary`), jamais un nom en toutes lettres, pour
rester valable d'un client à l'autre. Relancer cette commande après tout
changement de palette ou de nom tant que les vraies photos ne sont pas
intégrées. Une fois une vraie photo (ou un vrai logo) posé à la main, ne plus
relancer le script sur ce fichier précis (il écrase sans confirmation) — voir
`public/images/README.md`.

Convention complète des fichiers réels : `public/images/README.md`. En résumé,
remplacer tous les fichiers listés (chaque photo existe en deux largeurs,
`nom.webp` et `nom-960.webp`, sauf les exceptions documentées) :

- `logo.svg` (monogramme, régénéré par le script ci-dessus — voir aussi §7)
- `hero.webp` / `hero-mobile.webp` / `hero-960.webp`, `about.webp` (+ son
  palier `-1280`), `og-image.jpg` (JPEG, pas webp)
- `menu-pains.webp`, `menu-viennoiseries.webp`, `menu-patisseries.webp` (ou les
  catégories définies dans `config.ts`)
- `gallery-1.webp` à `gallery-6.webp` (ou le nombre défini dans `config.ts`)
- `map.webp` (voir §5)

**Vérification obligatoire avant intégration, sur *chaque* photo** (voir
CLAUDE.md § *Photos* — une devanture ou un prix concurrent visible est une
faute grave) :

- [ ] Aucune enseigne, logo ou texte de tiers lisible (menus, étiquettes de
      prix, panneaux — y compris en arrière-plan flou ou dans un miroir)
- [ ] Aucun prix affiché n'appartient à un autre commerce (attention aux
      étiquettes en devise ou langue étrangère, faciles à manquer)
- [ ] Recadrage portrait vérifié pour le rendu mobile
- [ ] Lumière cohérente avec le reste de la série (planche-contact)

Une photo qui échoue à l'un de ces points ne doit **jamais** être intégrée,
même temporairement — c'est plus risqué à oublier qu'à ne pas commencer.

## 4 bis. Détail produit (ingrédients, allergènes, et informations libres)

Chaque produit de `menu[].items[]` porte trois champs optionnels — n'utiliser
que ceux pertinents pour le métier du client, chacun ne s'affiche que s'il est
renseigné :

- `ingredients` : liste courte, dans l'ordre de la recette.
- `allergenes` : sous-ensemble du type `Allergene` (les 14 allergènes à
  déclaration obligatoire, règlement UE n°1169/2011 annexe II) — toujours le
  nom exact (ex. `"Céréales contenant du gluten"`), jamais un résumé du genre
  « contient des allergènes ». Mettre `[]` explicitement pour un produit sans
  aucun de ces 14 allergènes (distinct d'un champ absent, qui signifie
  « non renseigné »).
- `details` : liste libre de paires `{ label, value }`, affichées dans l'ordre
  donné. **Aucun libellé n'est prédéfini par le template** — chaque métier
  choisit les siens (voir tableau ci-dessous). C'est ce champ qui remplace
  d'anciens champs nommés (`origine`, `cuisson`, `entretien`) : trois noms
  fixes ne suffisaient pas à couvrir tous les métiers (ex. race, conservation,
  nombre de personnes pour une boucherie ; composition, durée de vie,
  toxicité pour les animaux chez un fleuriste).

Exemple par métier :

| Métier      | Champs à utiliser            | Exemple                                                                                   |
| ----------- | ----------------------------- | ------------------------------------------------------------------------------------------ |
| Boulangerie | `ingredients`, `allergenes`   | `allergenes: ["Céréales contenant du gluten", "Lait"]`                                     |
| Boucherie   | `details`                     | `details: [{ label: "Origine", value: "Bœuf — France, Aveyron" }, { label: "Cuisson", value: "12 min par kilo à 220 °C" }]` |
| Fleuriste   | `details`                     | `details: [{ label: "Composition", value: "10 roses, eucalyptus" }, { label: "Durée de vie", value: "7 à 10 jours" }, { label: "Toxicité animaux", value: "Toxique pour les chats" }]` |

`allergenes` et `ingredients` sont des affirmations réglementées ou de
traçabilité : **ne jamais les deviner pour de bon**, même si `config.ts` doit
contenir une valeur plausible à la livraison (voir CLAUDE.md § *Données
client*) — marquer chaque entrée `// À CONFIRMER avec le commerçant` et faire
valider la liste complète avant mise en ligne. La même prudence s'applique à
tout `details` qui touche à la traçabilité (origine, cuisson) ou à la sécurité
(toxicité) : à faire valider par le commerçant avant mise en ligne, pas à
deviner.

Ces champs alimentent automatiquement :

- leur affichage sous chaque produit dans la section Nos produits/Notre carte
  (`Menu.astro`) ;
- la page d'infos produits (voir `infoPage` ci-dessous), pensée pour être
  ouverte par QR code au comptoir ;
- le lien vers cette page dans le pied de page (`Footer.astro`) et celui en
  bas de la section Nos produits.

**`infoPage`** (`config.ts`, à côté de `menu`) configure cette page :

- `slug` : chemin d'URL, sans slashes. **Valeur par défaut du template :
  `"allergenes"` — ne pas la changer sans mettre à jour le QR code physique
  déjà imprimé** (voir §9).
- `title` : titre en haut de page (ex. `"Allergènes"`, `"Origine & cuisson"`,
  `"Entretien"`).
- `intro` : paragraphe d'introduction sous le titre — à adapter au métier (le
  texte par défaut du template mentionne l'affichage obligatoire en boutique,
  pertinent en boulangerie/restauration, pas forcément ailleurs).
- `linkLabel` : libellé du lien vers cette page, utilisé à la fois dans la
  section produits et dans le pied de page (ex. `"Allergènes"`,
  `"Origine & cuisson"`, `"Entretien"`).

**`allergenesValides: boolean`** (`config.ts`, à côté de `menu`) contrôle
l'affichage : tant qu'il vaut `false` (valeur par défaut du template), la
section Nos produits et la page d'infos produits affichent un bandeau rouge
« EXEMPLE — données non validées par le commerce, à titre de démonstration ».
**Ne passer `allergenesValides` à `true` qu'après relecture et validation
explicite du commerçant** — jamais par défaut, jamais pour « faire propre »
sur une démo. Une fois à `true`, le bandeau disparaît.

## 4 ter. Section Commandes (optionnelle)

`commandes` (`config.ts`, à côté de `menu`) ajoute une section « Commandes »
sur la page d'accueil (`Orders.astro`), pour un commerce qui prend des
commandes à l'avance (gâteau d'événement, bouquet composé, pièce de viande
sur mesure...). **Entièrement statique : aucune base de données, aucun suivi
de commande, aucun stock.** Le bouton « Appeler » et le formulaire ne font
qu'envoyer une demande par e-mail au commerçant (même mécanisme et même clé
que `forms.web3formsAccessKey`, voir §3) ; c'est au commerçant de rappeler
pour confirmer délai, prix et modalités de retrait — jamais un engagement
automatique.

**Mettre `commandes` à `undefined` (supprimer le bloc entier) si le commerce
ne prend pas de commandes à l'avance** : la section, le lien de menu et le
formulaire disparaissent alors complètement, sans rien à modifier ailleurs.

Champs :

- `title` : titre de la section, réutilisé tel quel comme libellé du lien de
  navigation vers `#orders` (`Header.astro`).
- `intro` : paragraphe d'introduction, sous le titre.
- `items[]` : ce qui peut être commandé, dans l'ordre d'affichage — chaque
  entrée a un `label`, un `delaiMinimum` (ex. `"48h"`, `"15 jours"`) et,
  si pertinent, une `quantiteMinimum` (ex. `"6 personnes"`).
- `noteForteDemande` (optionnel) : note sur les périodes de forte demande
  (ex. fêtes de fin d'année), affichée sous la liste si renseignée.

Le formulaire envoie nom, téléphone, produit (avec suggestions tirées de
`commandes.items[].label`, mais champ libre), quantité, date de retrait
souhaitée et remarques. Une mention fixe sous le formulaire rappelle que la
demande n'est pas une commande confirmée — ce texte est générique et ne se
configure pas.

## 5. Carte statique

`map.webp` est un assemblage de tuiles OpenStreetMap centré sur l'adresse du
commerce, sans iframe ni script tiers (voir `public/images/README.md`).
Régénérer pour la nouvelle adresse (nouvelles constantes `LAT`/`LON`), et
mettre à jour `config.ts` (`contact.address.lat/lng`, `map.staticImageAlt`).
L'attribution OpenStreetMap dans `map.attribution` est obligatoire, ne pas la
retirer.

**`map.webp` DOIT être régénéré pour chaque client, sans exception.** Le
template ne doit jamais contenir la carte centrée sur l'adresse réelle d'un
client — un incident déjà survenu : après « neutralisation » du template pour
en retirer les données d'un client précédent, `config.ts` avait bien été
remis à des valeurs génériques mais `map.webp` était resté celui du client
précédent, affichant en clair le nom de sa rue sur l'image. Voir §7 pour la
raison pour laquelle cette fuite est indétectable par recherche de texte.

## 6. Contrôle qualité complet

```bash
npm run build      # astro check + build de production
npm run contrast   # contraste WCAG AA
node screenshot.mjs # captures + axe-core — les regarder, pas seulement lire le résultat
npm run audit       # Lighthouse mobile + desktop, seuil 90 (relancer 2-3 fois, cf. CLAUDE.md)
```

Le hook pre-commit (§1) relance tout ça automatiquement à chaque commit.

## 7. Recherche des données du client précédent — zéro occurrence attendue

Dernière vérification avant livraison : confirmer qu'aucune trace du client
précédent ne subsiste dans le dépôt (fichiers, pas l'historique git). Chercher
chaque donnée identifiante de l'ancien commerce — nom, ville, téléphone,
adresse, domaine email :

```bash
rg -i "<nom ancien client>|<ville>|<téléphone>|<adresse>|<domaine email ancien client>" \
  --glob '!node_modules' --glob '!dist' --glob '!.git'
```

Exemple de forme (à remplacer par les vraies données du client que vous
sortez de ce dépôt avant de dupliquer pour le suivant) :

```bash
rg -i "Boulangerie Dupont|Nom de la ville|01 23 45 67 89|12 rue de l'Exemple" \
  --glob '!node_modules' --glob '!dist' --glob '!.git'
```

**Résultat attendu : zéro occurrence.** Si `rg` remonte quelque chose,
c'est une fuite à corriger avant de livrer — le plus souvent un fichier de
documentation (`README.md`, commentaire) qui donne l'ancienne adresse comme
exemple plutôt qu'un vrai bug de code, mais à vérifier au cas par cas.

**Cette recherche `rg` ne couvre que le texte.** Toute fuite contenue dans un
fichier binaire ou vectoriel (carte statique générée, photo, image OG, logo
SVG) lui échappe totalement — `rg` ne l'y verra jamais, même en cherchant le
bon mot-clé, y compris quand le texte est présent en clair dans le balisage
`<text>` d'un SVG. C'est arrivé concrètement deux fois : `map.webp` affichait
le nom de la rue d'un client précédent en toutes lettres sur l'image, et
`public/images/logo.svg` portait le nom d'un client précédent écrit dans une
balise `<text>` — dans les deux cas la recherche texte remontait zéro
occurrence. **Avant toute livraison ou démonstration à un prospect, ouvrir et
regarder `map.webp`, `og-image.jpg` et `logo.svg` à l'œil** — la recherche
automatisée ne remplace pas cette vérification visuelle pour ces fichiers.

## 8. Déploiement

`wrangler.jsonc` cible Cloudflare Pages/Workers, site entièrement pré-rendu
(pas de champ `main`, pas d'adaptateur `@astrojs/cloudflare` — uniquement les
assets statiques de `dist/`).

Création du projet Cloudflare (une fois par client, voir la règle en tête de
fichier — jamais réutiliser le projet Cloudflare d'un client précédent) :

1. Dans le compte Cloudflare : **Workers & Pages → Create application**,
   sélectionner le nouveau dépôt GitHub créé au §1.
2. Build command : `npm run build`
3. Deploy command : `npx wrangler deploy`
4. Variable d'environnement `NODE_VERSION` = `22`
5. Déployer, puis **vérifier l'URL obtenue sur mobile et sur desktop** avant
   de la considérer prête (voir §2 pour le cas où le domaine définitif n'est
   pas encore acheté).

## 9. Avant livraison

- **Générer et imprimer le QR code de la page d'infos produits**
  (`infoPage.slug`, `"allergenes"` par défaut — voir §4 bis), une fois le site
  déployé sur son URL finale (§8) :

  ```bash
  npm run qr -- https://www.nouveau-client.fr/allergenes/ public/images/qr-allergenes
  ```

  `scripts/qrcode.mjs` génère localement `public/images/qr-allergenes.svg` (vectoriel,
  net à toute taille d'impression) et `public/images/qr-allergenes.png` (2000px, haute
  résolution) — aucun service tiers, aucune redirection, aucun compte : le QR
  encode directement l'URL finale. Correction d'erreur au niveau H et zone de
  silence suffisante pour rester scannable même légèrement abîmé ou sali au
  comptoir. Remettre le PNG ou le SVG au commerçant pour impression (étiquette
  comptoir, table, vitrine) ; ne pas régénérer avec une URL provisoire
  (`workers.dev`), le QR imprimé doit pointer sur le domaine définitif.
- **`siteConfig.legal` NE se remplit PAS par client.** Il décrit l'identité
  légale de l'éditeur du site (l'agence/l'auto-entrepreneur qui conçoit et
  publie les sites, actuellement Tom Canal) — pas celle du commerçant, qui est
  déjà couverte par `business` et `contact`. Ce bloc reste identique d'un
  client à l'autre ; ne le modifier que si l'éditeur change (nouvelle
  structure juridique, déménagement...), jamais pour adapter un site à un
  nouveau commerçant.
- Vérifier que `/mentions-legales/` et `/politique-confidentialite/` ne
  contiennent aucun placeholder (`[... À REMPLIR]`) avant livraison — signe
  que `siteConfig.legal` n'a pas encore été complété pour l'éditeur.
- Vérifier qu'aucune balise `noindex` ni aucun blocage `robots.txt` hérité du
  développement ne subsiste sur le site livré.
- **Consigner le client dans le registre des sites** : domaine, registrar,
  date d'expiration, hébergeur, dépôt GitHub, accès à la fiche Google du
  commerce.
