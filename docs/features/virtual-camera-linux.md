# Caméra virtuelle Linux

**État : prototype disponible avec `v4l2loopback` et `pyvirtualcam`.**

## But

Rendre le flux composé par Meet Master sélectionnable comme source vidéo dans les logiciels de réunion sous Linux.

## Responsabilités attendues

- Recevoir des images composées dans un format et une cadence définis.
- Les publier sous forme d’un périphérique caméra accessible aux applications.
- Signaler clairement les prérequis système et les permissions nécessaires.
- Démarrer et arrêter proprement le périphérique, et expliquer les erreurs d’accès.

## Installation sous Debian / Ubuntu

Le module noyau `v4l2loopback` doit être installé avec les en-têtes correspondant exactement au noyau en cours, puis chargé :

```bash
sudo apt install v4l2loopback-dkms linux-headers-$(uname -r)
sudo modprobe v4l2loopback devices=1 exclusive_caps=1 card_label="Meet Master"
```

`exclusive_caps=1` aide les applications WebRTC à reconnaître le périphérique comme une caméra de capture après le démarrage du flux. `card_label` lui donne le nom **Meet Master**. Le chargement du module demande les droits administrateur ; Meet Master lui-même n’a pas besoin de tourner en administrateur. Si les en-têtes exacts ne sont pas disponibles dans les dépôts de ta distribution, installe ceux fournis par le mainteneur du noyau.

Installe ensuite l’extra Python du projet et démarre le flux :

```bash
python -m pip install -e ".[gestures,virtual-camera]"
meet-master preview --gestures --virtual-camera
```

La fenêtre locale reste visible pour les réglages, mais seule l’image composée (webcam ou vidéo d’absence et transition) est envoyée à la caméra virtuelle ; les textes de diagnostic restent dans l’aperçu. Meet Master affiche le chemin `/dev/videoN` ouvert. Si plusieurs périphériques loopback existent, sélectionne-en un avec `--virtual-camera-device /dev/videoN`.

Dans Meet, Zoom ou Teams, choisis **Meet Master** comme caméra. Avec le mode `exclusive_caps`, démarre Meet Master avant d’ouvrir la liste des caméras de l’application.

## Limites

- L’adaptateur actuel vise Linux ; il dépend du module noyau v4l2loopback et de ses en-têtes compatibles avec le noyau.
- La résolution et la cadence reprennent celles rapportées par la webcam ; le pilote du loopback et l’application de réunion négocient le format final.
- Fermer Meet Master arrête le flux et libère le périphérique.
- La sortie caméra virtuelle n’est pas encore implémentée sous Windows.

Le code d’envoi est isolé dans `platforms/linux/virtual_camera.py` et reste optionnel via l’extra `virtual-camera`.
