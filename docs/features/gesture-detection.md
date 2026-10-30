# Détection des gestes

**État : prototype disponible dans l’aperçu Linux.** Cette fonction affiche les résultats, mais ne déclenche aucune action.

## But

Reconnaître en temps réel une main et un geste afin de vérifier le modèle, le cadrage et la fiabilité avant de relier les gestes aux états d’absence et de retour.

## Comportement actuel

Lancer `meet-master preview --gestures` ouvre l’aperçu et affiche séparément chaque main détectée : côté gauche/droit et les trois meilleurs candidats avec leurs scores. Jusqu’à deux mains sont traitées par image. Une prédiction au-dessus du seuil est affichée en vert ; une prédiction plus faible est signalée, sans masquer le classement. Si la catégorie `None` est la meilleure, l’aperçu indique que le geste sort des catégories apprises. Le code n’émet aucune commande de changement d’état.

## Fonctionnement

Le cœur partagé convertit une trame BGR en RGB puis appelle MediaPipe Gesture Recognizer en mode vidéo avec `num_hands=2`. Les horodatages monotones croissants sont requis par cette API. Les résultats d’identité de main et de geste sont associés par leur index de détection et renvoyés comme une liste d’observations indépendantes de l’interface : côté, meilleur geste, score et classement. Le classificateur est configuré pour renvoyer toutes ses catégories et ne pas filtrer les scores en interne ; l’interface montre les trois premières. Cela rend les hésitations du modèle visibles. L’adaptateur Linux ne fait qu’afficher ces observations sur des lignes distinctes.

Pour `✌️`, `🤟` et `🤘`, le cœur vérifie aussi la flexion des doigts à partir des 21 points 3D de la main. Il mesure les angles des articulations index, majeur, annulaire, auriculaire et pouce. Comme ces angles ne dépendent pas de l’orientation de l’image, ces trois signes doivent rester reconnus lorsque la main est tournée. Les règles distinguent le V (index + majeur), le signe « I Love You » (index + auriculaire + pouce) et les cornes rock (index + auriculaire, pouce replié). Le choix est détaillé dans la [décision 0002](../decisions/0002-rotation-independent-hand-poses.md). La table complète des emojis et leurs besoins est dans le [catalogue des gestes](gesture-catalog.md).

MediaPipe précise que les côtés gauche/droit sont ceux de la personne et qu’une image inversée horizontalement inverse aussi la classification des côtés. Comme l’aperçu est miroir par défaut, Meet Master corrige les étiquettes dans ce mode. Avec `--no-mirror`, les côtés du flux brut sont conservés. Cette convention est décrite dans le [guide officiel Hand Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker).

Le modèle préentraîné reconnaît les catégories fournies par MediaPipe : poing fermé, paume ouverte, index pointé vers le haut, pouce vers le bas, pouce vers le haut, signe V et « I Love You ». Les noms et seuils proviennent de [l’API GestureRecognizerOptions](https://ai.google.dev/edge/api/mediapipe/python/mp/tasks/vision/GestureRecognizerOptions). Les trois règles géométriques ci-dessus ajoutent le signe des cornes et rendent ces poses indépendantes de la rotation.

## Installation et utilisation

```bash
python -m pip install -e '.[gestures]'
meet-master preview --gestures
```

Le seuil d’acceptation visuelle vaut `0.50` par défaut et se règle entre `0` et `1` :

```bash
meet-master preview --gestures --gesture-threshold 0.35
```

Un seuil plus bas marque davantage de candidats comme reconnus, mais augmente aussi les fausses reconnaissances. Les scores des trois meilleurs candidats restent affichés, même sous le seuil. En mode aperçu, le réglage sert seulement à l’affichage. Il faudra choisir et valider un seuil plus strict avant de relier un geste à une action. Le filtrage des classes est configurable par les options du [classificateur MediaPipe](https://ai.google.dev/edge/api/mediapipe/python/mp/tasks/components/processors/ClassifierOptions).

Au premier lancement, Meet Master télécharge le fichier officiel du modèle depuis [Google AI Edge](https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task) et le conserve dans `~/.cache/meet-master/gesture_recognizer.task` (ou `$XDG_CACHE_HOME/meet-master/`). Pour utiliser un fichier déjà téléchargé, passez `--model /chemin/vers/gesture_recognizer.task`.

Le modèle fourni reconnaît sept catégories prédéfinies : poing fermé, paume ouverte, index levé, pouce vers le bas, pouce levé, signe V et signe « I Love You ». Il ne peut pas reconnaître toutes les formes de main possibles. Pour les gestes personnalisés ou les variantes qui apparaissent comme « geste hors modèle », il faudra fournir et évaluer un modèle personnalisé ; baisser le seuil ne peut pas ajouter de nouvelles catégories.

## Données et confidentialité

L’image webcam est analysée localement par le modèle ; Meet Master ne l’envoie ni ne l’enregistre. L’installation du modèle nécessite un téléchargement initial, évitable avec l’option `--model`. MediaPipe indique que ses tâches traitent les images sur l’appareil et ne transmettent pas ces images à Google, mais indiquent aussi transmettre des métriques d’utilisation et de performance. Voir [l’avis de confidentialité MediaPipe Tasks](https://developers.google.com/edge/mediapipe/solutions/tasks#mediapipe_tasks_privacy_notice). La dépendance et ces métriques ne sont pas encore configurables dans Meet Master.

## Décisions ouvertes

- Sélection d’un geste de départ et d’un geste de retour qui ne se confondent pas dans l’usage quotidien.
- Confirmation temporelle et anti-répétition avant toute action.
- Seuil de confiance pour les commandes, durée de confirmation et anti-répétition.
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
