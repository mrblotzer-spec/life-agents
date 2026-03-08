from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path

from .config import Settings
from .demo_generator import create_demo_page
from .google_maps_client import GoogleMapsClient, dedupe_businesses
from .website_auditor import audit_website


@dataclass
class Lead:
    name: str
    place_id: str
    website: str | None
    phone_number: str | None
    address: str | None
    score: int
    grade: str
    reasons: list[str]
    demo_path: str | None = None


def run_pipeline(
    settings: Settings,
    *,
    latitude: float,
    longitude: float,
    radius_meters: int,
    keyword: str = "small business",
) -> dict[str, list[Lead]]:
    maps_client = GoogleMapsClient(settings.google_maps_api_key)
    businesses = maps_client.fetch_small_businesses(
        latitude=latitude,
        longitude=longitude,
        radius_meters=radius_meters,
        keyword=keyword,
    )
    businesses = dedupe_businesses(businesses)

    leads: list[Lead] = []
    weak: list[Lead] = []

    for business in businesses:
        audit = audit_website(business.website)
        lead = Lead(
            name=business.name,
            place_id=business.place_id,
            website=business.website,
            phone_number=business.phone_number,
            address=business.address,
            score=audit.score,
            grade=audit.grade,
            reasons=audit.reasons,
        )
        if lead.grade in {"D", "F"}:
            demo = create_demo_page(
                business,
                pricing_link=settings.stripe_price_link or "https://example.com/pricing",
                output_dir=f"{settings.output_dir}/demos",
            )
            lead.demo_path = str(demo)
            weak.append(lead)
        leads.append(lead)

    report = {
        "all_businesses": leads,
        "priority_outreach": weak,
    }
    save_report(report, Path(settings.output_dir) / "report.json")
    return report


def save_report(report: dict[str, list[Lead]], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    serializable = {
        key: [asdict(lead) for lead in value]
        for key, value in report.items()
    }
    destination.write_text(json.dumps(serializable, indent=2), encoding="utf-8")
