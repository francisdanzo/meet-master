# Guide de contribution

Ce guide aide une personne qui découvre le dépôt à comprendre comment proposer une modification.

## Avant de changer le code

1. Lisez le [README](../README.md) et cette architecture.
2. Ouvrez la fiche dans `docs/features/` correspondant à la fonction.
3. Regardez l’état de la fonction : disponible, en cours, ou à concevoir.
4. Si le comportement prévu n’est pas assez précis, écrivez d’abord la décision ou la question dans la fiche au lieu de coder une hypothèse silencieuse.

## Règles de structure

- Gardez les commandes et leur validation dans `cli.py`.
- Gardez le code spécifique à Linux ou Windows dans `platforms/<système>/`.
- Placez dans `core/` uniquement la logique qui ne doit pas connaître les périphériques ni le système.
- Une fonction partagée doit pouvoir recevoir des images ou des données en entrée sans ouvrir elle-même la webcam.
- Libérez les périphériques et fenêtres même en cas d’erreur ou d’interruption.
- Les messages destinés aux utilisateurs doivent expliquer quoi vérifier et, si possible, comment continuer.

## Documentation à mettre à jour

Pour toute nouvelle fonction ou tout changement de comportement :

1. Créez ou mettez à jour sa fiche sous `docs/features/`.
2. Décrivez le comportement observable, les étapes internes, les options, les erreurs, les limites et les données conservées.
3. Séparez les faits implémentés des idées futures.
4. Mettez à jour le tableau d’état dans le README si le statut change.
5. Mettez à jour `docs/architecture.md` si le flux ou une frontière entre modules change.

## Dépendances

Les dépendances nécessaires à l’exécution sont déclarées dans `pyproject.toml`. Évitez d’ajouter une bibliothèque pour une tâche qui tient clairement dans le code existant. Lorsqu’une dépendance est ajoutée, notez dans la fiche concernée pourquoi elle est nécessaire et si elle est limitée à une plateforme.

## État du projet et licence

Une fonction ne doit apparaître comme disponible dans le README que lorsqu’elle existe dans le code. Le dépôt n’ayant pas encore de licence, toute réutilisation doit attendre que le projet ait fait ce choix.
