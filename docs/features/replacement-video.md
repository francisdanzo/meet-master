# Vidéo de remplacement en boucle

**État : à concevoir.** Aucune vidéo n’est encore lue par Meet Master.

## But

Afficher une courte séquence préenregistrée pendant que l’utilisateur quitte le champ de la webcam, pour que l’appel continue avec une image choisie plutôt qu’un écran noir.

## Comportement visé

Après la transition de départ, le lecteur diffuse la vidéo de remplacement et reprend au début lorsqu’il atteint la fin. Au retour, la lecture est interrompue ou masquée par la transition de retour, puis la webcam reprend.

## Questions à résoudre

- Formats et résolutions acceptés, et stratégie de mise à l’échelle.
- Comment l’utilisateur choisit, prévisualise et remplace la vidéo.
- Que faire si le fichier est absent, illisible, sans image ou trop court.
- Si le son est ignoré ou pris en charge; la première version devrait privilégier une sortie vidéo silencieuse.
- Comment synchroniser la boucle avec la cadence de la caméra virtuelle.

## Données

La vidéo sera choisie localement par l’utilisateur. La fiche finale devra préciser si Meet Master copie le fichier ou se contente de le lire à son emplacement, et confirmer que le contenu n’est pas envoyé à un service distant.
