# Support & astuces — dépôt Wado

Ce fichier regroupe des **commandes** et **bonnes pratiques** utiles pour travailler sur le monorepo (notamment le site **`web/composites-webapp`**). Ce n’est pas une politique de support produit : pour les utilisateurs finaux du site, prévoir une page contact ou un canal dédié.

---

## Webapp Foil (`web/composites-webapp`)

```bash
cd web/composites-webapp
npm install
npm run dev
npm run lint
npm run build
```

Variables : voir le README du projet pour `NEXT_PUBLIC_SITE_URL`.

---

## Vidéo web (ffmpeg)

Astuces pour alléger une vidéo destinée au **hero** ou au streaming web (MP4 H.264, compatible navigateurs).

### MP4 H.264 + AAC, prêt pour le web (`faststart`)

Le flag `+faststart` déplace les métadonnées en tête du fichier pour un démarrage de lecture plus fluide.

```bash
ffmpeg -i entree.mov -c:v libx264 -profile:v high -pix_fmt yuv420p \
  -crf 24 -preset slow \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  sortie.mp4
```

- **`-crf`** : qualité (18–28 typique ; plus haut = fichier plus petit, plus compressé). Essayer `23`–`28` pour le web.
- **`-preset`** : `slow` = meilleure qualité / taille pour un même CRF (plus long à encoder). `medium` ou `fast` pour aller plus vite.

### Redimensionner (ex. hauteur max 720 px, largeur proportionnelle)

```bash
ffmpeg -i entree.mov -vf "scale=-2:720" -c:v libx264 -pix_fmt yuv420p \
  -crf 24 -preset slow -movflags +faststart -c:a copy sortie_720p.mp4
```

### Sans piste audio (fond visuel uniquement)

```bash
ffmpeg -i entree.mov -an -c:v libx264 -pix_fmt yuv420p \
  -crf 24 -preset slow -movflags +faststart sortie_sans_audio.mp4
```

### Extraire un extrait (10 s à partir de 5 s)

```bash
ffmpeg -ss 5 -i entree.mp4 -t 10 -c copy extrait.mp4
```

(Re-encoder si besoin de couper au frame près : retirer `-c copy` et repasser par `-c:v libx264` etc.)

### WebM (VP9) — option pour navigateurs modernes

```bash
ffmpeg -i entree.mov -c:v libvpx-vp9 -crf 35 -b:v 0 -row-mt 1 \
  -c:a libopus -b:a 96k sortie.webm
```

---

## Images (aperçus, OG)

### Réduire une PNG / JPEG avec ImageMagick

```bash
magick input.png -resize 1200x630^ -gravity center -extent 1200x630 output.png
```

### Squoosh (GUI)

[https://squoosh.app](https://squoosh.app) — comparaison visuelle WebP / AVIF / MozJPEG.

---

## Git — rappels utiles

```bash
git status
git diff
git log --oneline -n 15
```

Créer une branche et pousser :

```bash
git checkout -b feature/ma-fonctionnalite
git push -u origin feature/ma-fonctionnalite
```

---

## Ajouter une entrée ici

Quand tu retombes sur une commande utile (ffmpeg, `curl`, outils CLI du projet, déploiement), ajoute une courte section avec **contexte + exemple copiable**. Garde les blocs de commande **complets** (sans `...`).
