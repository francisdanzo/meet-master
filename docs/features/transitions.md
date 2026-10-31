# Transitions de disparition et de retour

**État : bascule présent/absent disponible dans l’aperçu Linux ; effets visuels à concevoir.**

## But

Rendre le passage de la webcam à la vidéo de remplacement, puis le retour à la webcam, intentionnel et lisible.

## Intention visuelle

L’utilisateur souhaite un effet cinématographique inspiré de la disparition en anime ou en comics. Le rendu doit rester compréhensible dans une petite vignette de réunion et ne pas gêner le geste de départ.

## Séquence visée

1. Le signe ✌️ confirmé bascule l’aperçu de présent à absent.
2. Le clip du fond enregistré au lancement (ou le fichier fourni avec `--away-video`) démarre et tourne en boucle.
3. Le signe ✌️ suivant revient à l’image webcam.

La vidéo en boucle est disponible dans l’aperçu. La caméra virtuelle et les effets de disparition/apparition restent à implémenter. Voir la [fiche de bascule présent/absent](presence-toggle.md) et la [fiche de la vidéo de remplacement](replacement-video.md).

## Choix à documenter avant implémentation

- Style graphique précis, durée et intensité.
- Effets basés sur l’image, particules ou masque animé.
- Image de départ figée ou webcam en mouvement pendant l’effet.
- Ordre de composition et comportement si la webcam n’a plus de trame.
- Respect des performances CPU et fréquence d’image.
- Réglage pour désactiver l’effet ou réduire son intensité.

Les effets devront être des composants réutilisables du cœur partagé et ne pas contenir de code propre à Linux ou Windows.
