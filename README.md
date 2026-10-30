# Meet Master

Meet Master est un projet de caméra virtuelle pour les réunions en ligne. Un geste de la main doit permettre de remplacer la webcam par une courte vidéo en boucle, avec des effets de disparition et de retour. Le projet est développé d’abord sous Linux, avec une intégration Windows prévue.

## État actuel

La première fonction disponible est l’aperçu local de la webcam sous Linux. Elle permet de vérifier l’accès caméra avant d’ajouter la détection des gestes et la caméra virtuelle.

| Fonctionnalité | État | Documentation |
|---|---|---|
| Aperçu webcam Linux | Disponible | [Guide de l’aperçu](docs/features/webcam-preview.md) |
| Détection des gestes | À concevoir | [Spécification](docs/features/gesture-detection.md) |
| Vidéo de remplacement en boucle | À concevoir | [Spécification](docs/features/replacement-video.md) |
| Transitions de disparition et de retour | À concevoir | [Spécification](docs/features/transitions.md) |
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
python -m meet_master --help
```

La résolution demandée dépend des modes pris en charge par la webcam et son pilote. L’aperçu ne sauvegarde pas les images, n’envoie aucune donnée sur le réseau et ne fournit pas encore de caméra virtuelle aux logiciels de réunion.

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
  contributing.md            règles pour contribuer et maintenir la doc
```

Voir [l’architecture](docs/architecture.md) et le [guide de contribution](docs/contributing.md) pour comprendre où ajouter une fonction.

## Contribuer

Les propositions et contributions sont les bienvenues. Avant de modifier une fonction, consultez sa fiche dans `docs/features/`. Toute modification visible par l’utilisateur doit mettre à jour la fiche concernée et le tableau d’état de ce README.

Le dépôt n’a pas encore de licence choisie. Il est public et consultable, mais les conditions de réutilisation du code restent à décider.
