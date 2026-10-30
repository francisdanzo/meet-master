# Décision 0002 : règles géométriques pour certaines poses de main

- **Statut :** adopté pour un prototype ciblé
- **Date :** 2026-10-30

## Contexte

Le modèle Gesture Recognizer de base ne garantit pas la reconnaissance des poses demandées lorsque la main est tournée. Les signes `✌️`, `🤟` et `🤘` sont définis principalement par les doigts tendus ou repliés, et cette forme ne devrait pas dépendre de l’orientation de la main dans l’image.

## Décision

Mesurer les angles 3D des articulations à partir des 21 repères de main MediaPipe. Utiliser des règles distinctes pour le V, le signe I Love You et les cornes rock, puis privilégier ces résultats sur le classement visuel du modèle.

## Conséquences

- Une règle par angles est invariante aux rotations rigides des coordonnées 3D.
- Les règles évitent de collecter un nouveau jeu de données pour ces trois poses.
- Les seuils d’angle sont initiaux et devront être ajustés avec des mains et angles variés.
- Cette approche ne différencie pas les mouvements temporels et ne suffit pas aux emojis à deux mains.
- Les autres gestes de la liste nécessitent des règles propres à leur forme, une mesure d’orientation, un suivi temporel ou un classificateur entraîné.

## À valider

Vérifier le V, le signe I Love You et les cornes avec la main verticale, inclinée et tournée de côté. Confirmer que les doigts partiellement repliés ne déclenchent pas ces classes par erreur.
