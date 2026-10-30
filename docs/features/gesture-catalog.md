# Catalogue des gestes emoji demandés

Cette page indique ce que le prototype classe déjà et ce qui reste à construire pour la liste d’emojis demandée. Les règles géométriques sont une première approximation et restent à valider sur la webcam, avec plusieurs mains et angles.

## Règles géométriques présentes dans le code

| Emojis | Classe affichée | Principe |
|---|---|---|
| ✌️ | V de victoire | Index et majeur tendus ; annulaire et auriculaire repliés. Indépendant de la rotation. |
| 🤟 | I Love You | Index, auriculaire et pouce tendus ; majeur et annulaire repliés. Indépendant de la rotation. |
| 🤘 | Cornes rock | Index et auriculaire tendus ; majeur, annulaire et pouce repliés. Indépendant de la rotation. |
| 👌 | Signe OK | Pouce et index rapprochés ; les autres doigts tendus. |
| 🤌 | Doigts pincés | Extrémités des doigts regroupées près du pouce. |
| 🤏 | Pincement pouce-index | Pouce et index rapprochés. |
| 👍 👎 | Pouce haut/bas | Pouce tendu ; direction estimée dans l’image. |
| ✊ | Poing fermé | Les quatre doigts sont repliés. |
| 🤞 | Doigts croisés | Index et majeur tendus et segments croisés dans la vue caméra. |
| 🖖 | Salut vulcain | Quatre doigts tendus avec un espace marqué entre majeur et annulaire. |
| 🖕 | Majeur levé | Majeur tendu ; les autres doigts repliés. |
| 👈 👉 👆 👇 ☝️ 🫵 | Pointage | Index tendu ; direction estimée à gauche, droite, haut, bas ou vers la caméra. |
| 🖐️ ✋ 🤚 | Main ouverte | Les quatre doigts tendus. Le dos/la paume et les variantes de salut ne sont pas encore séparés. |

Ces règles mesurent les angles articulaires 3D pour la forme des doigts et utilisent les repères 2D uniquement quand le geste dépend de la direction de l’écran. Les résultats marqués « forme » sont des correspondances de règles, pas des scores de probabilité appris.

## Gestes encore à ajouter ou différencier

| Emojis | Travail restant |
|---|---|
| 👋 | Détecter un mouvement de salut dans plusieurs images. |
| 🫰 | Distinguer le cœur de doigt du pincement à partir du croisement et de la séquence de pose. |
| 👊 🤛 🤜 | Séparer un poing dirigé vers la caméra des poings orientés à gauche/droite. |
| 🫱 🫲 🫳 🫴 | Estimer l’orientation de la paume et la direction de la main. |
| 👏 | Détecter un mouvement répété de rapprochement/contact des deux mains. |
| 🙌 👐 🤲 🙏 🫶 | Comparer la position, l’orientation et la forme des deux mains. |

## Limites de la classification

- `👋` et `👏` décrivent des mouvements : une image isolée ne suffit pas.
- `✋`, `🖐️` et `🤚` sont proches par la forme des doigts ; le dos ou la paume tournée vers la caméra aide à les distinguer.
- `👊`, `🤛` et `🤜` partagent un poing fermé et se distinguent par l’orientation ou le mouvement.
- Les emojis à deux mains exigent un suivi des deux mains, pas seulement deux prédictions indépendantes.
- Des poses personnalisées peuvent demander des exemples enregistrés et un classificateur entraîné.

## Prochaines étapes

1. Vérifier les règles actuelles pour des mains droites, inclinées et tournées de côté.
2. Ajuster leurs seuils pour réduire les confusions.
3. Ajouter les orientations de paume et les gestes directionnels manquants.
4. Ajouter la mémoire temporelle pour les saluts et applaudissements.
5. Ajouter un classificateur de relation entre les deux mains.
6. Valider chaque classe avec des exemples réels avant de l’utiliser pour déclencher une action.
