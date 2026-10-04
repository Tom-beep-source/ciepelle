# Ciepelle : bilan détaillé des 3 et 4 octobre 2026

À lire **en entier** au début de chaque nouvelle session, avec `RESUME-SESSION.md`.
Utilisateur : Tom.
- Parle-lui en français, sans jargon, avec peu de captures d'écran.
- Montants en zł avec l'équivalent en € (1 € ≈ 4,25 zł).
- **Il n'a plus de budget pour des outils** : l'argent restant est réservé aux pubs Meta.
- Les clientes sont **polonaises** : tout ce qu'elles voient doit être en polonais.

---

## 1. Où tout se trouve

| Quoi | Où |
|---|---|
| Dépôt GitHub | `Tom-beep-source/ciepelle`, branche **`claude/ciepelle-shopify-resume-vh7vey`** (tout le travail est là, pas sur `main`) |
| Contexte général du projet | `RESUME-SESSION.md` |
| Ce bilan | `BILAN-3-4-OCTOBRE.md` |
| Business plan, marges | `ciepelle-business/business-plan-meta.md`, `marges.md`, `marges.py`, `couts-fournisseurs.json` |
| Rapport d'audit + textes Meta (PL) | `RAPPORT-AUDIT-ET-META.md` |
| Kit page Facebook (bio, posts, visuels) | `meta-page/` (`KIT-PAGE-META.md`, `photo-profil.png`, `couverture-facebook.png`, `posts/`) |
| Pub « défilé » | `kling-defile/pub-defile-ciepelle.mp4` |
| Pub « essayage » | `kling-essayage/pub-essayage-ciepelle.mp4` |
| 5 variantes de pub A–E | `kling-variantes/sortie/ciepelle-variante-A…E.mp4` ; rendu : `./rendre.sh X` ; guide TikTok : `kling-variantes/TIKTOK.md` |
| Fichiers du thème Shopify | `ciepelle-theme/` |
| Connexion Meta (lecture seule) | Variables d'environnement cloud `META_ADS_TOKEN` et `META_AD_ACCOUNT_ID`. **Jamais dans le dépôt, qui est public.** |
| Connecteurs Claude | Shopify, TrendTrack, Kling (au niveau du compte claude.ai) |

---

## 2. Boutique (purrpeak.com, marque Ciepelle)

- **Thème v8** : prêt et **testé**. Le paiement s'ouvre en polonais et en PLN, via « Przejdź do kasy » comme via « Kup teraz ». **Pas encore publié : c'est à Tom de le faire.**
  - Comportement connu, laissé tel quel : « Kup teraz » ajoute l'article au panier existant.
- **Description SEO** du produit principal corrigée : elle cite maintenant les 3 couleurs (cielisty, czarny i szary).
- **Prix** (PLN) :

  | Grammage | 1 paire | 2 paires | 3 paires | Trio (3 couleurs) |
  |---|---|---|---|---|
  | 80 g | 79 zł | 119 zł | 149 zł | 149 zł |
  | 220 g | 99 zł | 149 zł | 189 zł | 189 zł |
  | 300 g | 119 zł | 179 zł | 229 zł | 229 zł |

- **Vrais coûts fournisseurs relevés le 4 octobre** (prix publics AliExpress, prudents) → `marges.md`.
  - Marge avant pub, avec TVA 23 % : de **32 zł (7,6 €)** pour 1 paire chair 80 g à **69 zł (16,2 €)** pour 3 paires noires 80 g.
  - Offre phare (2 paires chair 220 g) : **59 zł (13,8 €)**.
  - Trio : **49 / 41 / 36 zł** (11,5 / 9,7 / 8,5 €) en 80 / 220 / 300 g.
  - Sans TVA (franchise, à confirmer par un comptable) : environ +25 à +45 zł par commande.
- **DSers (4 octobre)** : 9 déclinaisons critiques (chair 300 g, gris 80 g, gris 220 g, en 1/2/3 paires) **basculées sur COZOK**, car Stone's Store n'avait presque plus de stock. Stocks Shopify mis à jour.
  - La synchronisation automatique des stocks DSers est payante (19,9 $/mois) : **non activée**.
  - Le Trio est aussi chez COZOK : **commande test obligatoire**.
- **Adresse légale** : obligatoire (droit UE et polonais, UOKiK). Elle apparaît seulement dans les pages légales.
  - Proposé, en attente de l'accord de Tom : une phrase rassurante en polonais sur la page Kontakt.

---

## 3. Domaine
- purrpeak.com (acheté chez IONOS) n'est pas cohérent avec la marque.
- **ciepelle.pl** est disponible (≈ 66 zł / 15,5 €, recommandé). ciepelle.com (≈ 58 zł) et ciepelle.store (≈ 33 zł) aussi.
- Tom demande à IONOS un remboursement ou un échange.
- **Décision : attendre le domaine final avant de l'utiliser dans Meta** (site de la page, pixel, vérification du domaine).

---

## 4. Meta : tout ce qui a été mis en place

1. **Page Facebook « Ciepelle »**
   - Créée le 3 octobre : couverture, bio en polonais.
   - Encore à faire :
     - remplacer la photo de profil par la version empilée (`meta-page/photo-profil.png`) ;
     - ajouter la catégorie « Marque de vêtements » ;
     - choisir le nom d'utilisateur @ciepelle.pl ;
     - publier les 6 posts de `meta-page/posts/`, 1 ou 2 par jour.
   - **Pas de site web sur la page tant que le domaine n'est pas choisi.**
2. **Ancienne page « AutoRec »** (projet d'il y a 3 ans) : restreinte par Meta, **on ne l'utilise pas**. À retirer du portefeuille business.
3. **Portefeuille business** (au nom de « tom canal ») : il contient la page Ciepelle, l'app de rapports et le compte pub.
4. **Ancien compte pub « AutoRec MINI »** : fermeture en cours. **Ne pas annuler la fermeture.**
5. **Nouveau compte publicitaire « Ciepelle PL »** : devise **EUR** (la carte de Tom est en euros, donc pas de frais de conversion), fuseau **Europe/Warsaw** (même heure que Paris). Actif, 0 € dépensé.
   - Les clientes voient tout en zł : la devise du compte ne concerne que la facture Meta.
   - **Carte et limite de dépense de 150 € pas encore ajoutées** : à faire à l'arrivée de la paye.
6. **App développeur « Ciepelle Rapports »**
   - Cas d'utilisation « API Marketing », autorisation **`ads_read` en accès standard**, app **non publiée** (normal).
   - ⚠️ Ne **jamais** accepter de devenir « Tech Provider » : c'est irréversible et inutile.
7. **Utilisateur système `claude-lecture`** (rôle Employé)
   - Accès au compte pub Ciepelle PL limité à « Afficher les performances », plus un rôle développeur sur l'app.
   - **Token en lecture seule (`ads_read`), testé avec succès le 4 octobre.**
   - **Il expire le 2 décembre 2026** : à régénérer avant (`claude-lecture` → « Générer un nouveau token » → app Ciepelle Rapports → 60 jours → `ads_read`), puis à remplacer dans les variables d'environnement.
8. **Environnement cloud Claude** (celui avec lequel le test a réussi) :
   - variables `META_ADS_TOKEN` et `META_AD_ACCOUNT_ID` ;
   - accès réseau « Personnalisé » avec `graph.facebook.com` (plus trendtrack et les autres domaines utiles).
   - **Démarrer les sessions Ciepelle dans cet environnement.**
   - Test rapide : lire `name,currency,timezone_name` sur `graph.facebook.com/v21.0/$META_AD_ACCOUNT_ID`. On ne lit que des informations, on ne modifie rien.
9. **Connecteur Meta pour Claude** : il n'existe pas de connecteur officiel. C'est l'accès par l'API ci-dessus qui le remplace.

---

## 5. Contenus créés

- **7 pubs vidéo en polonais** (9:16, 6 à 13 s, musique originale libre de droits, fin sur le logo et « Zestaw 3 par już od 149 zł ») :

  | Fichier | Accroche |
  |---|---|
  | `pub-defile-ciepelle.mp4` | « Wyglądają jak gołe nogi… a w środku polar. » |
  | `pub-essayage-ciepelle.mp4` | « Wyglądają jak zwykłe przezroczyste rajstopy, ale… » |
  | `ciepelle-variante-A.mp4` | « Sukienka zimą i nie marzniesz? » |
  | `ciepelle-variante-B.mp4` | « Jeden model. Trzy kolory. » |
  | `ciepelle-variante-C.mp4` | « POV: wszyscy myślą, że masz gołe nogi » |
  | `ciepelle-variante-D.mp4` | « Za oknem zima… a ona w cienkich rajstopach? » |
  | `ciepelle-variante-E.mp4` | « To nie są zwykłe rajstopy » |

- **Plan TikTok** : compte pro @ciepelle.pl, 1 vidéo par jour entre 18 h et 21 h (heure de Varsovie). La vidéo qui fait le plus de vues gratuites devient la 1ʳᵉ pub payante sur Meta.
- **Kit page Meta** : `meta-page/`. Il contient l'analyse TrendTrack des pages concurrentes. À retenir : les marques gagnantes ont de petites pages (Feelwonder, 415 mentions J'aime → 10,9 M de personnes touchées). Le concurrent polonais Polarove a vu ses pubs stoppées au bout de 3 jours.
- **Kling** : il reste environ 1 crédit. La version de la pub essayage **avec un visage visible** (≈ 230 crédits) attend le rechargement mensuel. Tom ne veut plus rien payer.

---

## 6. Prochaines étapes

**Dès maintenant (gratuit), côté Tom :**
1. Publier le thème v8.
2. Finir la page Facebook et publier les posts.
3. Ouvrir TikTok pro et publier les variantes.
4. Retirer AutoRec du portefeuille business.
5. Réponse d'IONOS sur le domaine.
6. Ajouter le fournisseur de secours dans DSers : Exquisite (AliExpress 1005006188489629).
7. Adresse complète de la boutique dans Shopify (pages légales).
8. Commande test, de préférence un Trio.
9. Validation de la TVA par un comptable.
10. Passer le dépôt GitHub en **privé**.

**Le jour de la paye :**
1. Domaine final, relié à Shopify.
2. App Facebook & Instagram dans Shopify : pixel, partage des données sur « Maximum », vérification du domaine.
3. Carte bancaire et limite de 150 € sur Ciepelle PL.
4. Campagne **Ventes Advantage+** :
   - Pologne, femmes 22–55 ans, **80 zł/jour (≈ 19 €)**, mention IA cochée ;
   - les 3 vidéos les plus vues sur TikTok ;
   - textes polonais dans `RAPPORT-AUDIT-ET-META.md`.
5. Bilans tous les 2 à 3 jours via l'API Meta, en lecture seule, avec les règles du business plan § 6.D :
   - couper une pub à 120 zł dépensés sans vente ;
   - +20 % de budget si le coût par vente reste sous 45 zł ;
   - arrêt à 560 zł dépensés sans aucune pub rentable.
