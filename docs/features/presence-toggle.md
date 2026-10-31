# Basculer présent/absent avec le signe V

**État : prototype dans l’aperçu Linux.** ✌️ fait passer l’état de présent à absent, puis le signe suivant fait revenir à présent.

## Comportement

- Meet Master démarre dans l’état **présent** à chaque lancement.
- Une main qui maintient le signe V (`Victory`) pendant au moins 0,35 seconde déclenche un changement d’état.
- Le majeur doit être clairement tendu pour que le geste soit un V. Une pose intermédiaire entre V et index levé n’entraîne aucune bascule.
- Le signe doit être absent pendant 0,25 seconde avant de pouvoir déclencher à nouveau. Tenir le V ne fait donc basculer l’état qu’une fois.
- Le même signe sert au départ et au retour : présent → absent → présent.
- Si deux mains montrent le V en même temps, le contrôleur ne bascule qu’une seule fois.

## Fonctionnement interne

`core/presence.py` reçoit les observations de chaque image, confirme la durée du signe, mémorise l’état et bloque les répétitions jusqu’au relâchement. Le module ne connaît ni OpenCV ni le périphérique caméra. L’adaptateur Linux dessine l’état dans l’aperçu.

## Essayer

```bash
meet-master preview --gestures
```

Au démarrage de `--gestures`, sors du champ cinq secondes pendant que Meet Master prépare le clip et la référence du fond. Montre ✌️ et maintiens-le brièvement : ta silhouette estimée se fragmente en mosaïque lumineuse avant de passer sur le clip en boucle, en laissant le décor tranquille. Relâche le signe, puis montre-le de nouveau pour révéler la silhouette webcam avec le même effet.

## Limites actuelles

- La carte d’absence est seulement un aperçu local. Les logiciels de réunion continuent de recevoir leur caméra habituelle, car la sortie caméra virtuelle n’est pas encore implémentée.
- La carte ne joue pas encore la vidéo de remplacement choisie par l’utilisateur.
- L’effet de disparition anime/comics n’est pas encore implémenté ; le passage à la carte est immédiat.
- L’état n’est pas conservé après fermeture ou redémarrage de Meet Master.
- Si la détection du signe V échoue, aucun changement d’état ne se produit. Les seuils et règles du signe sont décrits dans la [fiche des gestes](gesture-detection.md).

## Fichiers concernés

- `src/meet_master/core/presence.py` : état présent/absent, confirmation et anti-répétition.
- `src/meet_master/platforms/linux/webcam.py` : carte d’absence et aperçu.
