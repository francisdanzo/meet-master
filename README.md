# Meet Master

Meet Master est un projet de caméra virtuelle pour les réunions en ligne. Un geste de la main doit permettre de remplacer la webcam par une courte vidéo en boucle, avec des effets de disparition et de retour. Le projet est développé d’abord sous Linux, avec une intégration Windows prévue.

## État actuel

Le prototype permet de prévisualiser la webcam, détecter des gestes, basculer l’aperçu en absence avec ✌️ et lire un clip local en boucle pendant cette absence.

| Fonctionnalité | État | Documentation |
|---|---|---|
| Aperçu webcam Linux | Disponible | [Guide de l’aperçu](docs/features/webcam-preview.md) |
| Reconnaissance des gestes dans l’aperçu | Prototype disponible | [Fonctionnement et limites](docs/features/gesture-detection.md) |
| Basculer présent/absent avec ✌️ | Prototype Linux | [Fiche de la bascule](docs/features/presence-toggle.md) |
| Vidéo d’absence enregistrée automatiquement | Prototype Linux | [Fonctionnement et limites](docs/features/replacement-video.md) |
| Transitions mosaïque, fondu et flash sur la silhouette | Prototype Linux | [Fonctionnement et limites](docs/features/transitions.md) |
| Caméra virtuelle Linux | À concevoir | [Spécification](docs/features/virtual-camera-linux.md) |
| Intégration Windows | À concevoir | [Spécification](docs/features/windows.md) |

Les documents marquent explicitement les fonctions disponibles et celles qui sont encore des propositions. Une proposition ne doit pas être présentée comme un comportement déjà codé.

## Installation sous Linux

Prérequis : Python 3.10 ou supérieur, une webcam accessible, et une session graphique pour afficher la fenêtre OpenCV.

```bash
git clone https://github.com/francisdanzo/meet-master.git
cd meet-master
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Pour installer la reconnaissance gestuelle, ajoutez l’option correspondante :

```bash
python -m pip install -e '.[gestures]'
```

Si vous aviez installé la première version du projet, elle utilisait `opencv-python`. MediaPipe utilise `opencv-contrib-python`, et les deux distributions fournissent le même module `cv2`. Avant de mettre à jour cet ancien environnement, retirez l’ancienne distribution pour éviter les fichiers partagés en double :

```bash
python -m pip uninstall opencv-python
python -m pip install -e '.[gestures]'
```

Sous Debian, si la création de l’environnement virtuel indique que `venv` manque, installez le paquet système correspondant à votre version de Python (`python3-venv`), puis recréez l’environnement.

## Lancer l’aperçu webcam

```bash
meet-master preview
```

La commande ouvre la caméra d’index `0` en demandant une image de 1280 × 720 pixels. Par défaut, l’image est inversée horizontalement pour ressembler à un miroir. Appuyez sur `q` ou `Échap` pour fermer la fenêtre.

Options utiles :

```bash
meet-master preview --camera 1
meet-master preview --width 640 --height 480
meet-master preview --no-mirror
meet-master preview --gestures
meet-master preview --gestures --gesture-threshold 0.35
meet-master preview --gestures --model /chemin/vers/gesture_recognizer.task
meet-master preview --gestures --away-video /chemin/vers/ma-video.mp4
python -m meet_master --help
```

La résolution demandée dépend des modes pris en charge par la webcam et son pilote. En mode standard, l’aperçu ne sauvegarde pas les images et ne se connecte pas au réseau. Il ne fournit pas encore de caméra virtuelle aux logiciels de réunion.

Avec `--gestures`, le programme détecte jusqu’à deux mains, affiche les prédictions et utilise ✌️ pour basculer entre présent et absent. L’effet de transition s’applique à la silhouette estimée à partir du fond vide capturé au lancement. Choisis `--transition mosaic` (par défaut), `--transition fade` ou `--transition flash`. Au démarrage, le programme demande de sortir du champ, attend cinq secondes et enregistre trois secondes dans le cache Meet Master (`~/.cache/meet-master` sous Linux, `%LOCALAPPDATA%\MeetMaster\Cache` sous Windows) ; le clip tourne en boucle pendant l’absence et son sous-dossier de session est supprimé à la fermeture. `--away-video` permet de choisir un autre clip, mais la capture du fond reste nécessaire pour estimer la silhouette. L’effet est visible dans l’aperçu local : Zoom, Meet et Teams ne reçoivent pas encore ce flux. Consultez la [fiche des transitions](docs/features/transitions.md), la [fiche de la vidéo de remplacement](docs/features/replacement-video.md), la [fiche gestes](docs/features/gesture-detection.md) et le [catalogue des emojis](docs/features/gesture-catalog.md) pour les détails et limites.

## Structure du code

```text
src/meet_master/
  cli.py                    commandes et options
  core/                     logique partagée entre plateformes
  platforms/linux/           capture webcam et sortie Linux
  platforms/windows/         intégration Windows à venir
docs/
  architecture.md            flux de données et responsabilités
  features/                  fonctionnement et spécifications par fonction
  decisions/                 raisons des choix d’architecture
  contributing.md            règles pour contribuer et maintenir la doc
```

Voir [l’architecture](docs/architecture.md) et le [guide de contribution](docs/contributing.md) pour comprendre où ajouter une fonction.

## Contribuer

Les propositions et contributions sont les bienvenues. Avant de modifier une fonction, consultez sa fiche dans `docs/features/`. Toute modification visible par l’utilisateur doit mettre à jour la fiche concernée et le tableau d’état de ce README.

Le dépôt n’a pas encore de licence choisie. Il est public et consultable, mais les conditions de réutilisation du code restent à décider.
