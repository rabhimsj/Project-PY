from __future__ import annotations

import argparse
import sys

from .ui import run_app


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TaskFlow Manager")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without opening the desktop UI.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.headless:
        print("TaskFlow Manager is ready to run.")
        return 0

    try:
        run_app()
    except Exception as exc:  # pragma: no cover - UI startup failure is surfaced to the user
        print(f"Unable to start the TaskFlow Manager UI: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
