# Vidéo de remplacement en boucle

**État : prototype dans l’aperçu Linux.** Un fichier vidéo local peut remplacer l’image caméra dans l’aperçu quand l’état passe à absent.

## Utiliser

```bash
meet-master preview --gestures --away-video /chemin/vers/ma-video.mp4
```

`--away-video` nécessite `--gestures`, car le signe V commande le départ et le retour. Le chemin peut être relatif ou absolu. Sans fichier, Meet Master garde la carte d’absence sombre.

## Comportement

- Le clip commence à sa première image au passage présent → absent.
- À la fin du fichier, le lecteur revient au début et continue en boucle.
- La vidéo est mise à l’échelle pour tenir dans la résolution de la webcam, sans recadrage ; les bandes latérales ou supérieure/inférieure sont sombres.
- Le geste V continue d’être détecté depuis les images de la webcam en arrière-plan. Le retour à l’état présent reprend l’image webcam.
- La vidéo est silencieuse : OpenCV lit les images, pas la piste audio.

## Fonctionnement interne

`core/video_loop.py` ouvre le fichier par `cv2.VideoCapture`, lit la cadence indiquée par le fichier et conserve la dernière image décodée jusqu’à la prochaine échéance. Cela évite de jouer le clip à la cadence de lecture de la webcam. Si le décodeur n’indique pas de cadence plausible, le lecteur utilise 25 images/s. En fin de fichier, la position est replacée à l’image zéro.

Les propriétés de position, de cadence et de taille dépendent du backend vidéo et du codec installés ; voir la [documentation OpenCV des propriétés vidéo](https://docs.opencv.org/4.13.0/d4/d15/group__videoio__flags__base.html).

## Erreurs et limites

- Le fichier doit exister et être décodable par le backend OpenCV installé. Si OpenCV ne peut pas ouvrir le codec, Meet Master affiche une erreur plutôt que de démarrer sans clip.
- Le comportement du son est actuellement silence ; aucune piste audio n’est transmise ou jouée.
- Le clip ne sort pour l’instant que dans la fenêtre d’aperçu locale. Il n’est pas encore envoyé aux applications de réunion.
- Il n’y a pas encore de transition de disparition ni de fondu entre le clip et la webcam.
- La lecture ne modifie pas le fichier et n’envoie pas son contenu sur le réseau.

## Fichiers concernés

- `src/meet_master/core/video_loop.py` : décodage, cadence, boucle et mise à l’échelle.
- `src/meet_master/platforms/linux/webcam.py` : choix caméra/clip selon l’état présent/absent.
- `src/meet_master/cli.py` : option `--away-video`.
