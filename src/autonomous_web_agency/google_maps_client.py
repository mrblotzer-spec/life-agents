from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import requests


NEARBY_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"


@dataclass
class Business:
    name: str
    place_id: str
    address: str | None
    phone_number: str | None
    website: str | None
    rating: float | None
    user_ratings_total: int | None


class GoogleMapsClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_small_businesses(
        self,
        *,
        latitude: float,
        longitude: float,
        radius_meters: int,
        keyword: str = "small business",
    ) -> list[Business]:
        params = {
            "location": f"{latitude},{longitude}",
            "radius": radius_meters,
            "keyword": keyword,
            "key": self.api_key,
        }
        nearby = requests.get(NEARBY_URL, params=params, timeout=20)
        nearby.raise_for_status()
        payload = nearby.json()

        results = []
        for entry in payload.get("results", []):
            details = self._fetch_details(entry["place_id"])
            results.append(details)
        return results

    def _fetch_details(self, place_id: str) -> Business:
        params = {
            "place_id": place_id,
            "fields": "name,place_id,formatted_address,website,formatted_phone_number,rating,user_ratings_total",
            "key": self.api_key,
        }
        resp = requests.get(DETAILS_URL, params=params, timeout=20)
        resp.raise_for_status()
        result = resp.json().get("result", {})
        return Business(
            name=result.get("name", "Unknown"),
            place_id=result.get("place_id", place_id),
            address=result.get("formatted_address"),
            phone_number=result.get("formatted_phone_number"),
            website=result.get("website"),
            rating=result.get("rating"),
            user_ratings_total=result.get("user_ratings_total"),
        )


def dedupe_businesses(items: Iterable[Business]) -> list[Business]:
    seen: set[str] = set()
    unique: list[Business] = []
    for item in items:
        if item.place_id in seen:
            continue
        seen.add(item.place_id)
        unique.append(item)
    return unique
