# Architecture

Ce document explique comment le dépôt est organisé et comment une image doit traverser le programme. Les mécanismes marqués « prévu » ne sont pas encore implémentés.

## Principes

1. **Le cœur ne dépend pas du système.** Il contiendra les états de présence, les règles de geste et la composition des effets.
2. **Les appareils restent dans les adaptateurs de plateforme.** L’ouverture d’une webcam et la publication d’une caméra virtuelle diffèrent selon Linux et Windows.
3. **Une fonction documentée doit correspondre au code réel.** Les spécifications futures sont identifiées comme telles.
4. **Le traitement reste local par défaut.** La prévisualisation actuelle ne sauvegarde pas et n’envoie pas les images.

## Flux visé

```text
Webcam (adaptateur de plateforme)
        ↓ image brute
Reconnaissance de geste (cœur partagé, optionnelle dans l’aperçu)
        ↓ état : présent / départ / absent / retour
Composition vidéo (cœur partagé)
        ↓ webcam, transition ou vidéo de remplacement
Caméra virtuelle (adaptateur de plateforme)
        ↓
Zoom / Meet / Teams ou autre application
```

Aujourd’hui, la capture webcam Linux, la reconnaissance gestuelle, la bascule de présence et la lecture en boucle d’un clip local dans l’aperçu sont codées. Les effets et les sorties caméra virtuelle restent des étapes futures.

## Organisation

- `src/meet_master/cli.py` : options de commande et sélection de l’adaptateur. Il ne doit pas contenir le traitement d’image.
- `src/meet_master/core/` : types et logique qui doivent pouvoir être réutilisés par les deux plateformes, dont le client de reconnaissance gestuelle MediaPipe.
- `src/meet_master/core/video_loop.py` : lecture à cadence contrôlée, redémarrage au début et mise à l’échelle avec bandes sans recadrage.
- `src/meet_master/platforms/linux/` : accès Linux à la webcam, puis à la sortie caméra virtuelle.
- `src/meet_master/platforms/windows/` : futur accès Windows. Garder les détails Windows hors du cœur.
- `docs/features/` : fiche par fonctionnalité avec son état, son comportement, ses limites et les décisions encore ouvertes.

## Aperçu Linux actuel

1. La commande `meet-master preview` vérifie le système puis importe l’adaptateur Linux.
2. `webcam.preview()` ouvre l’index choisi avec le backend V4L2 d’OpenCV.
3. La largeur et la hauteur sont demandées au pilote. Le pilote peut choisir une autre résolution.
4. Chaque image BGR est éventuellement inversée horizontalement, annotée, puis affichée dans une fenêtre locale.
5. `q` ou `Échap` arrête la boucle. Le bloc `finally` libère la webcam et ferme les fenêtres OpenCV.

Avec `--gestures`, chaque trame caméra est envoyée au reconnaisseur partagé. Celui-ci convertit BGR en RGB, appelle MediaPipe en mode vidéo avec un horodatage monotone et renvoie une observation typée. Des règles sur les angles articulaires 3D peuvent remplacer le classement du modèle pour des signes choisis. `core/presence.py` confirme le signe V, bascule l’état présent/absent et impose un relâchement avant une nouvelle bascule. Au lancement, `platforms/linux/background_capture.py` enregistre le fond et calcule sa référence dans un sous-dossier de session du cache utilisateur (`core/cache.py`). `core/foreground.py` estime la silhouette par différence avec cette référence ; `core/frame_transition.py` applique l’effet choisi. En absence, `core/video_loop.py` lit le clip capturé ou le fichier passé avec `--away-video` en boucle. Si `--virtual-camera` est actif, `platforms/linux/virtual_camera.py` envoie l’image composée, sans les textes d’aperçu, au périphérique v4l2loopback. La webcam continue en arrière-plan pour détecter le geste de retour, puis le sous-dossier de session et le périphérique producteur sont libérés à la fermeture.

## Prochaines frontières à stabiliser

- Une interface commune de capture qui fournit les images et leur horodatage.
- Un format de trame commun pour que les adaptateurs puissent alimenter le composeur.
- Une sortie caméra avec démarrage, arrêt, gestion des erreurs et cadence définis.
- Le comportement si la main ou le geste n’est pas reconnu, afin d’éviter une bascule accidentelle.

Le choix MediaPipe pour la reconnaissance est consigné dans [la décision 0001](decisions/0001-mediapipe-gesture-recognizer.md). Le backend de caméra virtuelle reste à choisir.
