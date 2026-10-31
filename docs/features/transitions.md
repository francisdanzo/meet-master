# Transitions de disparition et de retour

**État : fondu en mosaïque disponible dans l’aperçu Linux.**

## But

Rendre le passage de la webcam à la vidéo de remplacement, puis le retour à la webcam, intentionnel et lisible.

## Intention visuelle

L’utilisateur souhaite un effet cinématographique inspiré de la disparition en anime ou en comics. Le rendu doit rester compréhensible dans une petite vignette de réunion et ne pas gêner le geste de départ.

## Séquence

1. Le signe ✌️ confirmé bascule l’aperçu de présent à absent.
2. L’image webcam se fragmente en petites cases lumineuses pendant environ 700 ms, puis le clip du fond enregistré au lancement (ou le fichier fourni avec `--away-video`) tourne en boucle.
3. Au signe ✌️ suivant, le même effet révèle l’image webcam à partir du clip.

La bordure des fragments reçoit un éclat cyan et blanc, tandis que les textes d’état restent nets au premier plan. Le composant partagé `core/frame_transition.py` gère l’effet et peut être réutilisé par les futurs adaptateurs Windows. Voir la [fiche de bascule présent/absent](presence-toggle.md) et la [fiche de la vidéo de remplacement](replacement-video.md).

## Limites et travail restant

- L’effet fragmente toute l’image, car la silhouette de la personne n’est pas encore détourée du fond.
- Le clip cible continue de changer pendant la transition ; l’image source reste figée au déclenchement.
- Il n’y a pas encore d’option pour désactiver l’effet ou régler sa durée.
- Les effets sont visibles dans l’aperçu local ; la caméra virtuelle Linux reste à implémenter.

Une prochaine amélioration pourra isoler la silhouette afin que seuls la personne et ses contours se dissipent, en laissant l’arrière-plan immobile.
