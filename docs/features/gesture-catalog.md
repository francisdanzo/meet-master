# Catalogue des gestes emoji demandés

Ce catalogue sépare les poses statiques que l’on peut reconnaître sur une image des gestes qui exigent une orientation précise, deux mains ou une séquence dans le temps. Le modèle de base MediaPipe ne couvre pas toute cette liste.

## Déjà ciblés par une règle géométrique indépendante de la rotation

| Emoji | Nom affiché | Forme de doigts utilisée |
|---|---|---|
| ✌️ | V de victoire | Index et majeur tendus ; annulaire et auriculaire repliés |
| 🤟 | Signe I Love You | Index, auriculaire et pouce tendus ; majeur et annulaire repliés |
| 🤘 | Cornes rock | Index et auriculaire tendus ; majeur, annulaire et pouce repliés |

Ces règles utilisent les angles articulaires 3D de MediaPipe, pas la direction verticale de l’image. Ce sont des règles initiales à valider avec des angles de main différents.

## Dans le modèle de base ou à distinguer plus finement

| Emojis | Pose à reconnaître | Travail restant |
|---|---|---|
| 👋 🤚 🖐️ ✋ | Main ouverte | Reconnaître le mouvement de salut et distinguer paume/dos ; certaines variantes partagent la même pose statique |
| 🖖 | Salutation vulcaine | Détecter la séparation entre majeur/annulaire et les autres doigts |
| 👌 🤌 🤏 🫰 | Pincements | Mesurer les distances relatives entre pouce et doigts, puis différencier les configurations proches |
| 👍 👎 | Pouce haut/bas | Détecter un pouce tendu et son orientation dans l’image |
| ✊ 👊 🤛 🤜 | Poing | Reconnaître poing fermé et orientation du poing ; plusieurs emojis sont le même poing tourné différemment |
| 🤞 | Doigts croisés | Détecter le croisement réel des segments index/majeur |
| 🖕 | Doigt d’honneur | Majeur tendu, autres doigts repliés |
| 👈 👉 👆 👇 ☝️ 🫵 | Pointage | Reconnaître l’index puis sa direction dans l’image ou vers la caméra |
| 🫱 🫲 🫳 🫴 | Main orientée | Distinguer direction de la main et orientation de la paume |
| 👏 | Applaudissement | Détecter le rapprochement et l’éloignement répétés des deux mains |
| 🙌 👐 🤲 🙏 🫶 | Signes à deux mains | Détecter les relations entre mains : hauteur, paumes rapprochées, forme en cœur ou paumes vers le haut |

## Pourquoi une image ne suffit pas toujours

- `👋` signifie souvent un mouvement de salut : plusieurs images successives sont nécessaires.
- `👏` est un mouvement de contact répété, pas seulement deux mains visibles.
- `✋` et `🖐️` ont des poses statiques très proches ; la distinction dépend du contexte ou du modèle emoji choisi.
- `👊`, `🤛` et `🤜` sont tous des poings fermés ; les différencier exige d’analyser l’orientation et le mouvement.
- `🙏`, `🤲`, `👐`, `🙌` et `🫶` exigent de détecter et comparer deux mains.
- Une règle par angles reconnaît une forme de doigts, mais ne peut pas apprendre de nouvelles catégories de gestes. Pour les catégories personnalisées, il faudra enregistrer des exemples ou entraîner un classificateur adapté.

## Étapes de réalisation

1. Valider les règles d’angles pour `✌️`, `🤟` et `🤘` dans plusieurs orientations.
2. Ajouter des règles géométriques pour les poses à une main non ambiguës.
3. Ajouter l’orientation de la paume et les directions de pointage.
4. Suivre les deux mains dans le temps pour `👋`, `👏` et les poses à deux mains.
5. Évaluer chaque catégorie avec des exemples réels avant de l’activer comme geste de commande.
