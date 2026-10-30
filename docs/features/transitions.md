# Transitions de disparition et de retour

**État : à concevoir.** Aucun effet n’est encore implémenté.

## But

Rendre le passage de la webcam à la vidéo de remplacement, puis le retour à la webcam, intentionnel et lisible.

## Intention visuelle

L’utilisateur souhaite un effet cinématographique inspiré de la disparition en anime ou en comics. Le rendu doit rester compréhensible dans une petite vignette de réunion et ne pas gêner le geste de départ.

## Séquence visée

1. Le geste confirmé déclenche une transition depuis l’image webcam.
2. La transition se termine sur la vidéo de remplacement.
3. La boucle continue jusqu’au geste de retour.
4. Une transition de retour révèle la webcam.

## Choix à documenter avant implémentation

- Style graphique précis, durée et intensité.
- Effets basés sur l’image, particules ou masque animé.
- Image de départ figée ou webcam en mouvement pendant l’effet.
- Ordre de composition et comportement si la webcam n’a plus de trame.
- Respect des performances CPU et fréquence d’image.
- Réglage pour désactiver l’effet ou réduire son intensité.

Les effets devront être des composants réutilisables du cœur partagé et ne pas contenir de code propre à Linux ou Windows.
