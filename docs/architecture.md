# Architecture initiale

Le projet est organisé en trois couches :

- **Cœur partagé** : états de présence, interprétation des gestes et séquencement des transitions.
- **Traitement vidéo partagé** : composition de l’image réelle, des effets et de la vidéo de remplacement.
- **Adaptateurs de plateforme** : capture webcam et publication du flux comme caméra virtuelle.

Les API de caméra virtuelle étant différentes selon le système, les intégrations Linux et Windows restent isolées derrière une interface commune. Le premier prototype cible Linux.
