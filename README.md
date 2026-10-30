# meet-master

Meet Master est un projet de caméra virtuelle qui remplace temporairement l’image d’une réunion par une vidéo en boucle, déclenchée par un geste de la main. Des transitions de disparition et d’apparition donnent l’impression que la personne s’éclipse puis revient.

Le développement commence sur Linux (Debian), avec une architecture prévue pour ajouter Windows.

## État du projet

Le dépôt contient le squelette initial. La détection des gestes, les effets vidéo et les sorties caméra restent à construire.

## Démarrage

Python 3.10 ou supérieur est requis.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m meet_master
```

## Structure

```text
src/meet_master/
  core/       logique partagée (états, gestes, transitions)
  platforms/  intégrations propres aux systèmes d’exploitation
    linux/    capture et caméra virtuelle Linux
    windows/  intégration Windows
```

## Feuille de route

- [ ] Afficher et vérifier le flux de la webcam sous Linux
- [ ] Détecter un geste de départ et un geste de retour
- [ ] Jouer une transition puis une vidéo de remplacement en boucle
- [ ] Exposer le flux comme caméra virtuelle Linux
- [ ] Ajouter la sortie caméra sous Windows

Les contributions et retours sont les bienvenus. Les modalités de licence seront ajoutées quand le projet aura choisi sa licence.
