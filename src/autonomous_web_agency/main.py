from __future__ import annotations

import argparse

from dotenv import load_dotenv

from .config import load_settings
from .pipeline import run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Autonomous local-business web upgrade pipeline")
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lng", type=float, required=True)
    parser.add_argument("--radius", type=int, default=5000)
    parser.add_argument("--keyword", type=str, default="small business")
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    settings = load_settings()

    report = run_pipeline(
        settings,
        latitude=args.lat,
        longitude=args.lng,
        radius_meters=args.radius,
        keyword=args.keyword,
    )
    print(
        f"Processed {len(report['all_businesses'])} businesses, "
        f"generated {len(report['priority_outreach'])} demo leads."
    )


if __name__ == "__main__":
    main()
