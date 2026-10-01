# CLAUDE.md

Ce fichier guide Claude Code (claude.ai/code) dans ce dépôt.

## Ce qu'est ce dépôt

Template de site vitrine réutilisable pour un commerce local (boulangerie,
pâtisserie, restaurant). **Toutes les données métier vivent dans
`src/config.ts`** : dupliquer le projet et modifier ce seul fichier doit suffire
à obtenir le site d'un autre client. Aucun nom, horaire, prix, texte ou chemin
d'image ne doit être codé en dur dans `src/components` ou `src/pages`.

Stack : Astro 5 + Tailwind + GSAP/ScrollTrigger + Lenis.

## Réutilisable vs propre au client

Deux catégories strictes. Un fichier réutilisable qui contient une donnée
métier est un bug, même discret (voir l'exemple des polices ci-dessous).

**Réutilisable (le template)** — aucune donnée métier, copié tel quel d'un
client à l'autre :

- `src/components/*.astro`, `src/layouts/*.astro`, `src/pages/*.astro`
- `src/lib/*.ts` (helpers génériques : images, animations, lenis, jsonld)
- `src/styles/global.css` — n'utilise que des variables CSS injectées depuis
  la config (`--color-*`, `--font-*`), jamais une couleur ou une police en dur
- `scripts/*.mjs`, `screenshot.mjs`, `.githooks/*`
- `astro.config.mjs`, `tsconfig.json`, `package.json` — **à l'exception du
  champ `site` d'astro.config.mjs** (voir ci-dessous)

**Propre au client** — toute donnée métier vit ici, rien ailleurs :

- `src/config.ts` — la totalité : identité, palette, **polices (noms ET URLs
  des feuilles de style — voir `theme.fonts`)**, coordonnées, horaires, menu,
  galerie, avis, infos pratiques, carte, clé de formulaire (`web3formsAccessKey`),
  SEO
- `public/images/*` — toutes les photos (convention de nommage :
  `public/images/README.md`)
- `wrangler.jsonc` — le champ `name` (identifiant du déploiement Cloudflare)
- `astro.config.mjs` — le champ `site` (domaine du client)

**Piège déjà rencontré :** les URLs Google Fonts/Fontshare et les noms de
police étaient codés en dur dans `BaseLayout.astro` (un fichier réutilisable),
et `theme.fonts.heading`/`body` dans `config.ts` ne servaient à rien — les
changer n'aurait rien changé au rendu. Corrigé : `theme.fonts.preconnect` et
`theme.fonts.stylesheets` portent maintenant les URLs, `BaseLayout.astro` les
consomme génériquement. Pour changer de police sur un nouveau client, tout se
passe dans `config.ts`.

**Vérification de la séparation :** toute chaîne qui identifie CE client (nom,
ville, téléphone, adresse, email, horaires, texte d'avis...) trouvée ailleurs
que dans `src/config.ts` est un bug — voir `NOUVEAU-CLIENT.md` pour la
commande de recherche exacte à lancer avant de livrer un nouveau site.

## Commandes

```bash
npm run dev        # serveur de développement
npm run build      # astro check + build de production
npm run audit      # Lighthouse mobile + desktop, affiche les 4 scores
npm run contrast   # vérifie les couples texte/fond contre WCAG AA
npm run placeholders # régénère les aplats provisoires (voir § Photos) depuis config.ts
npm run qr -- <url> <fichier>  # génère un QR code SVG+PNG (voir NOUVEAU-CLIENT.md §9)
node screenshot.mjs # captures desktop + mobile, avec audit axe-core
```

## Direction artistique

Trois adjectifs, dans cet ordre de priorité : **artisanal, chaleureux, épuré**.
Jamais rustique, jamais cliché — pas de blé stylisé, pas de bois vieilli, pas de
tableau noir à craie, pas de « fait avec amour ».

Références visuelles : papeterie japonaise, Aesop, Kinfolk.

Règles fermes :

- **Deux polices maximum** par site. Une pour les titres, une pour le texte.
- **Deux couleurs + un neutre.** Pas de troisième couleur d'accentuation.
- Beaucoup d'espace blanc. En cas de doute, augmenter l'espacement.
- **Titres alignés à gauche.** Pas de titres centrés, pas de sur-titres en
  petites capitales espacées au-dessus des titres — c'est daté.
- **Une animation par section maximum.** L'animation souligne, elle ne décore
  pas.

## Photos

- **Jamais de banque d'images (Unsplash ou autre).** Une devanture ou un prix
  concurrent visible sur le site d'un client est une faute grave, et plusieurs
  photos Unsplash de boulangeries affichent une enseigne réelle, parfois dans
  une langue étrangère. Tant que les vraies photos du commerce ne sont pas
  fournies, utiliser `npm run placeholders` (aplats générés dans la palette du
  client, voir `public/images/README.md`) plutôt qu'une photo de tiers.
- **Jamais de texte, logo ou enseigne visible** sur une photo intégrée.
- Lumière chaude, cohérente d'une image à l'autre. Assembler une planche-contact
  pour juger la cohérence de la série, pas les images une par une.
- **Vérifier le recadrage en portrait** avant validation : une image qui
  fonctionne en 16:9 peut devenir illisible une fois recadrée pour le mobile.
- Format `.webp`, 1920px maximum, avec une variante `-960` (voir
  `public/images/README.md`).

## Contraintes techniques

- **Contraste WCAG AA partout** (4,5:1 texte courant, 3:1 grand texte et
  éléments d'interface). `npm run contrast` le vérifie.
- **Corps de texte : 17px minimum en mobile**, 18px à partir de 640px.
  L'utilitaire `.text-body` porte ce plancher.
- **Lighthouse > 90 sur les quatre catégories**, en mobile comme en desktop.
- `curl` toujours avec `--max-time 30` — une commande ne doit jamais pouvoir
  rester bloquée.
- Pas d'iframe ni de script tiers (carte, widgets d'avis) : ils font chuter le
  score de performance. La carte est une image statique locale.

## Vérification

**Vérifier via `getComputedStyle` plutôt qu'à l'œil sur une capture.** Une
capture pleine page fortement réduite fausse le jugement : des textes y semblent
trop sombres, des espacements trop grands, alors que les valeurs calculées sont
correctes. À l'inverse, elle masque de vrais défauts.

Deux pièges déjà rencontrés dans ce dépôt :

- Les modificateurs d'opacité Tailwind (`bg-surface/90`) exigent des couleurs en
  canaux RVB avec `<alpha-value>`. Avec une couleur hex dans une variable CSS,
  ils calculent silencieusement `rgba(0,0,0,0)` — l'élément n'a aucun fond, et
  rien ne le signale.
- Une capture prise avant le déclenchement du `loading="lazy"` photographie des
  emplacements vides. `screenshot.mjs` défile puis attend le chargement effectif.
- **Un Chrome fraîchement lancé contre un serveur qui vient de démarrer donne un
  score Performance mobile artificiellement bas** (caches disque/serveur/polices
  froids sur la toute première navigation) : `scripts/audit.mjs` chauffe donc
  Chrome avec une passe Lighthouse jetée avant la mesure réelle. Sans cette
  chauffe, le score oscillait entre 80 et 92 d'une exécution à l'autre sur la
  même build ; avec elle, il est stable (~93-94 mesuré sur ce template).

## Process

**Toujours lancer `screenshot.mjs` et regarder les captures avant de rendre la
main.** Regarder, pas seulement constater que le script s'est terminé.

Les contrôles qualité (contraste, axe-core, Lighthouse) tournent automatiquement
avant chaque commit via le hook `.githooks/pre-commit`. Pour les activer sur une
nouvelle copie du dépôt :

```bash
git config core.hooksPath .githooks
```

En cas d'urgence, `SKIP_QA=1 git commit ...` contourne le hook — à n'utiliser
que sciemment.

## Données client

Ne jamais inventer une donnée de commerce réel (téléphone, email, horaires,
avis). Si une information manque, mettre un commentaire explicite dans
`src/config.ts` (`// À CONFIRMER avec le commerçant`) plutôt qu'une valeur
plausible. Les avis de démonstration portent `// FICTIF` et ne doivent jamais
être présentés comme réels ni accompagnés d'une note chiffrée.
