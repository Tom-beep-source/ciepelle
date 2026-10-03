#!/bin/sh
# Rend une variante : timeline -> musique -> montage -> fichier léger dans sortie/
set -e; V=$1; cd "$(dirname "$0")"
python3 variantes.py $V
(cd audio && python3 music.py >/dev/null && ffmpeg -v error -y -i bande-son-defile.wav -af "volume=7.6dB,alimiter=limit=0.85:attack=3:release=60:level=disabled" -c:a aac -b:a 192k bande-son-defile.m4a && rm bande-son-defile.wav)
(cd montage && python3 montage.py >/dev/null && ffmpeg -v error -y -i defile-master.mp4 -c:v libx264 -preset slow -crf 22 -tune grain -maxrate 12M -bufsize 24M -pix_fmt yuv420p -c:a copy -movflags +faststart ../sortie/ciepelle-variante-$V.mp4 && rm defile-master.mp4)
echo "ok $V"
