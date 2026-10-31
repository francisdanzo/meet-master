"""Command-line interface for Meet Master.

Commands are intentionally thin: argument parsing lives here, while camera
access and image processing belong to platform adapters and the shared core.
"""

from __future__ import annotations

import argparse
import sys


def _confidence_score(value: str) -> float:
    """Parse a confidence score in the closed interval [0, 1]."""
    try:
        score = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("le score doit être un nombre entre 0 et 1") from error
    if not 0.0 <= score <= 1.0:
        raise argparse.ArgumentTypeError("le score doit être compris entre 0 et 1")
    return score


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
    preview.add_argument(
        "--gesture-threshold", type=_confidence_score, default=0.50, metavar="SCORE",
        help="score minimal d’un geste reconnu, de 0 à 1 (défaut : 0.50)",
    )
    preview.add_argument(
        "--away-video", metavar="FICHIER",
        help="utiliser ce clip pendant l’absence (nécessite --gestures ; le fond est toujours capturé)",
    )
    preview.add_argument(
        "--transition",
        choices=("fade", "flash"),
        default="fade",
        metavar="EFFET",
        help="effet sur la silhouette : fade ou flash (défaut : fade ; nécessite --gestures)",
    )
    return parser


def main() -> int:
    """Parse arguments and run the selected platform command."""
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "preview":
        if not sys.platform.startswith("linux"):
            parser.error("la prévisualisation webcam est actuellement disponible sous Linux uniquement")
        if args.away_video and not args.gestures:
            parser.error("--away-video nécessite aussi --gestures")
        if args.transition != "fade" and not args.gestures:
            parser.error("--transition nécessite aussi --gestures")

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
                gesture_threshold=args.gesture_threshold,
                away_video_path=args.away_video,
                transition_style=args.transition,
            )
        except RuntimeError as error:
            print(f"Erreur : {error}", file=sys.stderr)
            return 1

    parser.error("commande inconnue")
    return 2
