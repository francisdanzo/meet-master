"""Command-line interface for Meet Master.

Commands are intentionally thin: argument parsing lives here, while camera
access and image processing belong to platform adapters and the shared core.
"""

from __future__ import annotations

import argparse
import sys


def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser so help text stays the single source of truth."""
    parser = argparse.ArgumentParser(
        prog="meet-master",
        description="Caméra de remplacement pilotée par gestes pour les réunions.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    preview = commands.add_parser(
        "preview",
        help="afficher le flux de la webcam pour vérifier la capture",
        description="Ouvre une fenêtre d’aperçu webcam. Appuyez sur q ou Échap pour quitter.",
    )
    preview.add_argument(
        "--camera", type=int, default=0, metavar="INDEX",
        help="index de la webcam (défaut : 0)",
    )
    preview.add_argument(
        "--width", type=int, default=1280, metavar="PIXELS",
        help="largeur demandée en pixels (défaut : 1280)",
    )
    preview.add_argument(
        "--height", type=int, default=720, metavar="PIXELS",
        help="hauteur demandée en pixels (défaut : 720)",
    )
    preview.add_argument(
        "--no-mirror", action="store_true",
        help="ne pas inverser l’image horizontalement",
    )
    preview.add_argument(
        "--gestures", action="store_true",
        help="reconnaître et afficher les gestes (nécessite l’extra [gestures])",
    )
    preview.add_argument(
        "--model", metavar="FICHIER",
        help="utiliser un modèle MediaPipe local au lieu du téléchargement automatique",
    )
    return parser


def main() -> int:
    """Parse arguments and run the selected platform command."""
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "preview":
        if not sys.platform.startswith("linux"):
            parser.error("la prévisualisation webcam est actuellement disponible sous Linux uniquement")

        # Import lazily so importing the CLI or requesting --help does not
        # require an active graphical session or camera device.
        from meet_master.platforms.linux.webcam import preview

        try:
            return preview(
                camera_index=args.camera,
                width=args.width,
                height=args.height,
                mirror=not args.no_mirror,
                recognize_gestures=args.gestures,
                model_path=args.model,
            )
        except RuntimeError as error:
            print(f"Erreur : {error}", file=sys.stderr)
            return 1

    parser.error("commande inconnue")
    return 2
