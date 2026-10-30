# Détection des gestes

**État : prototype disponible dans l’aperçu Linux.** Cette fonction affiche les résultats, mais ne déclenche aucune action.

## But

Reconnaître en temps réel une main et un geste afin de vérifier le modèle, le cadrage et la fiabilité avant de relier les gestes aux états d’absence et de retour.

## Comportement actuel

Lancer `meet-master preview --gestures` ouvre l’aperçu et affiche séparément chaque main détectée : côté gauche/droit, geste reconnu et score. Jusqu’à deux mains sont traitées par image. Une main avec un score inférieur à 0,65 est indiquée comme incertaine. Le code n’émet aucune commande de changement d’état.

## Fonctionnement

Le cœur partagé convertit une trame BGR en RGB puis appelle MediaPipe Gesture Recognizer en mode vidéo avec `num_hands=2`. Les horodatages monotones croissants sont requis par cette API. Les résultats d’identité de main et de geste sont associés par leur index de détection et renvoyés comme une liste d’observations indépendantes de l’interface : côté, geste retenu, score et candidat. L’adaptateur Linux ne fait qu’afficher ces observations sur des lignes distinctes.

MediaPipe précise que les côtés gauche/droit sont ceux de la personne et qu’une image inversée horizontalement inverse aussi la classification des côtés. Comme l’aperçu est miroir par défaut, Meet Master corrige les étiquettes dans ce mode. Avec `--no-mirror`, les côtés du flux brut sont conservés. Cette convention est décrite dans le [guide officiel Hand Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker).

Le modèle préentraîné reconnaît les catégories fournies par MediaPipe : poing fermé, paume ouverte, index pointé vers le haut, pouce vers le bas, pouce vers le haut, signe V et « I Love You ». Les noms et seuils proviennent de [l’API GestureRecognizerOptions](https://ai.google.dev/edge/api/mediapipe/python/mp/tasks/vision/GestureRecognizerOptions).

## Installation et utilisation

```bash
python -m pip install -e '.[gestures]'
meet-master preview --gestures
```

Au premier lancement, Meet Master télécharge le fichier officiel du modèle depuis [Google AI Edge](https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task) et le conserve dans `~/.cache/meet-master/gesture_recognizer.task` (ou `$XDG_CACHE_HOME/meet-master/`). Pour utiliser un fichier déjà téléchargé, passez `--model /chemin/vers/gesture_recognizer.task`.

Si le score est inférieur à `0.65`, le geste n’est pas affiché comme reconnu. Le seuil est actuellement fixé dans le cœur ; il sera exposé comme option quand nous aurons évalué son comportement sur plusieurs conditions de lumière et de cadrage.

## Données et confidentialité

L’image webcam est analysée localement par le modèle ; Meet Master ne l’envoie ni ne l’enregistre. L’installation du modèle nécessite un téléchargement initial, évitable avec l’option `--model`. MediaPipe indique que ses tâches traitent les images sur l’appareil et ne transmettent pas ces images à Google, mais indiquent aussi transmettre des métriques d’utilisation et de performance. Voir [l’avis de confidentialité MediaPipe Tasks](https://developers.google.com/edge/mediapipe/solutions/tasks#mediapipe_tasks_privacy_notice). La dépendance et ces métriques ne sont pas encore configurables dans Meet Master.

## Décisions ouvertes

- Sélection d’un geste de départ et d’un geste de retour qui ne se confondent pas dans l’usage quotidien.
- Confirmation temporelle et anti-répétition avant toute action.
- Seuil de confiance, durée de confirmation et anti-répétition.
- Comportement si la main est occultée, hors champ ou mal détectée.
- Coût processeur sur des machines sans accélérateur dédié.
- Vérification que l’analyse reste locale et n’enregistre pas les images.

## Critères d’acceptation à fixer

La fiche devra décrire comment éviter les déclenchements accidentels, comment l’utilisateur comprend qu’un geste a été reconnu et comment suspendre la détection. Le modèle fourni n’est pas un interprète de langue des signes et ne devrait pas être utilisé à cette fin.

## Dépannage

- Si MediaPipe manque, installez l’extra `.[gestures]` dans l’environnement virtuel activé.
- Si le téléchargement initial échoue, vérifiez la connexion ou fournissez le fichier avec `--model`.
- Si aucune main n’est détectée, améliorez la lumière, placez la main entièrement dans le champ et essayez de la rapprocher de la caméra.
- Si le geste varie, maintenez la main immobile quelques instants. Le mode actuel n’effectue pas encore de confirmation temporelle.

## Fichiers concernés

- `src/meet_master/core/gesture_recognizer.py` : chargement du modèle, conversion des trames et observation partagée.
- `src/meet_master/platforms/linux/webcam.py` : affichage de l’observation.
- `src/meet_master/cli.py` : option `--gestures` et chemin `--model`.
- `pyproject.toml` : dépendance facultative MediaPipe.
