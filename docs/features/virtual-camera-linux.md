# Caméra virtuelle Linux

**État : à concevoir.** Le dépôt ne publie pas encore de périphérique caméra virtuelle.

## But

Rendre le flux composé par Meet Master sélectionnable comme source vidéo dans les logiciels de réunion sous Linux.

## Responsabilités attendues

- Recevoir des images composées dans un format et une cadence définis.
- Les publier sous forme d’un périphérique caméra accessible aux applications.
- Signaler clairement les prérequis système et les permissions nécessaires.
- Démarrer et arrêter proprement le périphérique, et expliquer les erreurs d’accès.

## Décisions ouvertes

- Backend de caméra virtuelle et compatibilité avec les sessions X11/Wayland.
- Installation ou chargement d’un module noyau éventuel.
- Format pixel, résolution, cadence, nom de périphérique.
- Possibilité de fonctionner sans privilèges administrateur.
- Comportement quand l’application de réunion ouvre ou ferme la caméra.

Le backend sera isolé dans `platforms/linux/` derrière le même contrat de sortie que l’intégration Windows.
