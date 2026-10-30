# Intégration Windows

**État : prévue, non implémentée.** L’application actuelle indique que la commande d’aperçu ne fonctionne que sous Linux.

## But

Permettre à la personne qui démarre sous Linux de retrouver le même comportement dans son installation Windows en dualboot.

## Ce qui doit rester partagé

- États de présence et commandes de changement d’état.
- Interprétation des résultats du détecteur de gestes.
- Règles de composition et comportement des effets.
- Gestion de la vidéo de remplacement et paramètres utilisateur, dans la mesure où les bibliothèques le permettent.

## Ce qui sera propre à Windows

- Capture de la webcam et découverte des périphériques.
- Publication du flux comme caméra virtuelle.
- Installation, permissions, lancement et arrêt de l’adaptateur.

## À vérifier avant le portage

- API de caméra virtuelle disponible et mode d’installation attendu.
- Compatibilité des logiciels de réunion ciblés.
- Emballage de l’application et stratégie de distribution.
- Reprise des paramètres et fichiers utilisateur entre les sessions, si souhaitée.
