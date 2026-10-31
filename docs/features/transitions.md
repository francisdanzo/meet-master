# Transitions de disparition et de retour

**État : fondu et flash limités à la silhouette estimée, disponibles dans l’aperçu Linux.**

## But

Rendre le passage de la webcam à la vidéo de remplacement, puis le retour à la webcam, intentionnel et lisible.

## Intention visuelle

L’utilisateur souhaite un effet cinématographique inspiré de la disparition en anime ou en comics. Le rendu doit rester compréhensible dans une petite vignette de réunion et ne pas gêner le geste de départ.

## Séquence

1. Le signe ✌️ confirmé bascule l’aperçu de présent à absent.
2. L’image webcam se fragmente en petites cases lumineuses pendant environ 700 ms, puis le clip du fond enregistré au lancement (ou le fichier fourni avec `--away-video`) tourne en boucle.
3. Au signe ✌️ suivant, le même effet révèle l’image webcam à partir du clip.

Les textes d’état restent nets au premier plan. Au lancement, le programme calcule une image de référence à partir du fond vide. `core/foreground.py` compare ensuite la webcam à cette référence et garde la plus grande zone modifiée ; `core/frame_transition.py` applique l’effet dans ce masque. Voir la [fiche de bascule présent/absent](presence-toggle.md) et la [fiche de la vidéo de remplacement](replacement-video.md).

## Choisir l’effet

```bash
meet-master preview --gestures --transition fade
meet-master preview --gestures --transition flash
```

- `fade` : la silhouette s’efface ou se révèle en douceur, avec un contour adouci et sans halo. C’est le réglage par défaut.
- `flash` : un éclat blanc souligne brièvement la silhouette pendant son fondu.

Les deux effets durent environ 700 ms et sont appliqués au masque de la personne uniquement. Le choix s’applique dans les deux sens.

## Limites et travail restant

- La segmentation par différence de fond est une estimation : elle peut inclure une ombre ou manquer des vêtements proches de la couleur du décor. Un changement d’éclairage ou un déplacement de caméra peut la perturber.
- La plus grande zone modifiée est considérée comme la personne ; les objets mobiles ou un cadrage décentré peuvent donc réduire la précision.
- Le clip cible continue de changer pendant la transition ; l’image source reste figée au déclenchement.
- Il n’y a pas encore d’option pour désactiver l’effet ou régler sa durée.
- Les effets sont visibles dans l’aperçu local ; la caméra virtuelle Linux reste à implémenter.

Une segmentation dédiée aux personnes pourra remplacer la différence de fond si ces limites gênent les essais.
