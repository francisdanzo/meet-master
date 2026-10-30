# Détection des gestes

**État : à concevoir.** Aucun modèle ni geste n’est actuellement implémenté.

## But

Permettre de déclencher l’absence et le retour sans cliquer dans l’application de réunion.

## Comportement visé

La détection devrait reconnaître un geste volontaire, configurable et suffisamment distinct des mouvements ordinaires. Un geste confirmé devrait provoquer une seule commande de changement d’état, même si la main reste visible plusieurs images.

## Fonctionnement envisagé

Un détecteur analysera les images de la webcam et retournera une observation structurée (geste, score de confiance, horodatage). Le cœur décidera si cette observation est assez fiable et cohérente dans le temps pour déclencher une action. L’adaptateur de caméra ne décidera pas lui-même si la personne est absente.

## Décisions ouvertes

- Bibliothèque et modèle de détection adaptés à Linux et Windows.
- Gestes de départ et de retour, et possibilité de les configurer.
- Seuil de confiance, durée de confirmation et anti-répétition.
- Comportement si la main est occultée, hors champ ou mal détectée.
- Coût processeur sur des machines sans accélérateur dédié.
- Vérification que l’analyse reste locale et n’enregistre pas les images.

## Critères d’acceptation à fixer

La fiche devra décrire comment éviter les déclenchements accidentels, comment l’utilisateur comprend qu’un geste a été reconnu et comment suspendre la détection.
