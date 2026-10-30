# Décision 0001 : MediaPipe pour la reconnaissance gestuelle

- **Statut :** adopté pour le prototype
- **Date :** 2026-10-30

## Contexte

Meet Master doit reconnaître des gestes à partir de la webcam, d’abord sous Linux et ensuite sous Windows. Le projet doit fonctionner sans envoyer les images vidéo vers un service distant, et la reconnaissance ne doit pas dépendre du code de capture Linux.

## Décision

Utiliser le Gesture Recognizer de MediaPipe Tasks en mode vidéo, avec le modèle officiel préentraîné. La dépendance MediaPipe est facultative (`pip install -e '.[gestures]'`) pour garder l’installation minimale de l’aperçu plus légère. Le projet utilise `opencv-contrib-python`, requis par MediaPipe, pour éviter d’installer deux distributions OpenCV qui fournissent le même module `cv2`. Le modèle n’est pas versionné dans Git : il est téléchargé une fois dans le cache utilisateur, ou peut être fourni avec `--model`.

## Raisons

- L’API Python prend en charge Linux et Windows ainsi que Python 3.9 et versions ultérieures selon le guide officiel.
- Le modèle comprend des classes de gestes courantes utiles pour un premier essai.
- L’inférence des images a lieu localement sur l’appareil selon l’avis MediaPipe Tasks.
- Le cœur peut recevoir des trames sans ouvrir lui-même le périphérique caméra.

Sources : [installation Python et plateformes prises en charge](https://developers.google.com/edge/mediapipe/solutions/setup_python), [API GestureRecognizerOptions](https://ai.google.dev/edge/api/mediapipe/python/mp/tasks/vision/GestureRecognizerOptions), [modèle officiel](https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task).

## Conséquences et limites

- Le premier lancement du mode gestuel nécessite une connexion pour télécharger le modèle, sauf si `--model` est fourni.
- MediaPipe indique aussi transmettre des métriques d’utilisation et de performance à Google. Le projet ne transmet pas lui-même les trames, mais ne configure pas encore ces métriques. Cette information doit rester visible dans la documentation utilisateur.
- Le modèle reconnaît des catégories prédéfinies ; les gestes de départ et de retour restent à choisir et à filtrer pour éviter les déclenchements accidentels.
- La qualité et les performances doivent être essayées sur le matériel visé avant de déclarer la reconnaissance prête à piloter l’état de l’application.
- La version majeure de MediaPipe est limitée à `<1.0` jusqu’à ce que le projet vérifie l’API des futures versions.

## Révision de la décision

Réévaluer cette décision si le modèle est instable sur les gestes retenus, si le coût CPU est trop élevé, si les métriques distantes ne conviennent pas au projet ou si une solution équivalente offre une meilleure compatibilité et confidentialité.
