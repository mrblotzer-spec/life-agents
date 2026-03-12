from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AuditResult:
    score: int
    grade: str
    reasons: list[str]


GRADE_SCALE = [(90, "A"), (80, "B"), (70, "C"), (60, "D"), (0, "F")]


def grade_from_score(score: int) -> str:
    for threshold, grade in GRADE_SCALE:
        if score >= threshold:
            return grade
    return "F"


def audit_website(url: str | None) -> AuditResult:
    if not url:
        return AuditResult(score=0, grade="F", reasons=["No website available"])

    try:
        import requests
        from bs4 import BeautifulSoup

        response = requests.get(url, timeout=12, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except Exception as exc:  # network/timeout/SSL errors
        return AuditResult(score=20, grade="F", reasons=[f"Website unreachable: {exc}"])

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    score = 40
    reasons: list[str] = []

    viewport = soup.find("meta", attrs={"name": "viewport"})
    if viewport:
        score += 15
    else:
        reasons.append("No viewport meta (likely not mobile-optimized)")

    if soup.find("section") or soup.find("header"):
        score += 10
    else:
        reasons.append("Minimal semantic HTML structure")

    if len(html) > 15000:
        score += 10
    else:
        reasons.append("Very thin content footprint")

    has_https = url.lower().startswith("https://")
    if has_https:
        score += 10
    else:
        reasons.append("Site is not HTTPS")

    has_cta = any(
        phrase in html.lower()
        for phrase in ["book now", "call now", "contact us", "get quote", "schedule"]
    )
    if has_cta:
        score += 10
    else:
        reasons.append("No clear call-to-action text found")

    if soup.find("script", src=True):
        score += 5

    score = max(0, min(100, score))
    return AuditResult(score=score, grade=grade_from_score(score), reasons=reasons)
