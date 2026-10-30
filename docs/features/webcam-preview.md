# Aperçu webcam Linux

**État : disponible.** Cette fonction est le premier jalon du projet.

## But

Afficher en direct la caméra choisie dans une fenêtre sur le bureau afin de vérifier la capture et son cadrage.

## Lancer

```bash
meet-master preview
meet-master preview --camera 1 --width 640 --height 480
meet-master preview --no-mirror
```

Les options disponibles sont aussi indiquées par `meet-master preview --help`.

## Fonctionnement

La commande transmet les options à `platforms/linux/webcam.py`. Cet adaptateur ouvre l’index avec le backend V4L2 d’OpenCV, demande une résolution, puis lit les trames une à une. Par défaut, chaque trame est inversée horizontalement comme dans un miroir. Un court texte d’aide est dessiné sur l’image avant l’affichage.

La capture se termine avec `q` ou `Échap`. Le bloc de nettoyage libère l’appareil et détruit les fenêtres OpenCV même si la lecture échoue.

## Options

- `--camera INDEX` choisit l’index OpenCV, `0` par défaut. Cet index n’est pas toujours égal au numéro indiqué dans le nom d’un fichier `/dev/videoN`.
- `--width PIXELS` et `--height PIXELS` indiquent une résolution souhaitée. Le pilote peut ne pas l’accepter.
- `--no-mirror` conserve l’orientation fournie par la caméra.

## Données et confidentialité

Les images circulent dans la mémoire du processus pour être affichées. Cette fonction ne les enregistre pas et ne les transmet pas sur le réseau. Fermer la fenêtre arrête la capture.

## Limites et dépannage

- Linux avec un backend V4L2 et une session graphique sont nécessaires.
- Si l’index `0` ne fonctionne pas, essayez `--camera 1`, puis d’autres index disponibles.
- Si une autre application utilise la caméra, fermez-la avant de relancer l’aperçu.
- Si l’accès est refusé, vérifiez les permissions des périphériques vidéo et votre appartenance au groupe `video`, puis reconnectez votre session après tout changement de groupe.
- Si OpenCV ne peut pas ouvrir de fenêtre, vérifiez que la commande est lancée depuis une session de bureau, et non depuis un terminal sans affichage graphique.
- La caméra intégrée peut apparaître comme plusieurs nœuds `/dev/video*`; tous ne sont pas nécessairement des flux vidéo utilisables.

## Fichiers concernés

- `src/meet_master/cli.py` : paramètres et messages destinés à l’utilisateur.
- `src/meet_master/platforms/linux/webcam.py` : ouverture, lecture, aperçu et nettoyage.
- `pyproject.toml` : dépendance OpenCV.
