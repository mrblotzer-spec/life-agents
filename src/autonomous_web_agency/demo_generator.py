from __future__ import annotations

from pathlib import Path

from jinja2 import Template

from .google_maps_client import Business


DEMO_TEMPLATE = Template(
    """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>{{ business.name }} | Modern Business Website Demo</title>
    <style>
      body { font-family: Inter, Arial, sans-serif; margin:0; color:#111827; }
      .hero { background:#111827; color:white; padding:4rem 1rem; text-align:center; }
      .container { max-width:960px; margin:0 auto; padding:2rem 1rem; }
      .card { border:1px solid #E5E7EB; border-radius:12px; padding:1rem; margin-top:1rem; }
      .btn { background:#2563EB; color:white; text-decoration:none; padding:.75rem 1rem; border-radius:8px; display:inline-block; }
    </style>
  </head>
  <body>
    <section class=\"hero\">
      <h1>{{ business.name }}</h1>
      <p>A modernized, conversion-focused website demo.</p>
      <a class=\"btn\" href=\"#contact\">Request This Site</a>
    </section>
    <main class=\"container\">
      <div class=\"card\">
        <h2>About</h2>
        <p>{{ business.name }} proudly serves the local community with trusted service and a customer-first experience.</p>
      </div>
      <div class=\"card\">
        <h2>Contact</h2>
        <p>{{ business.address or 'Serving your area' }}</p>
        <p>{{ business.phone_number or 'Call for appointment' }}</p>
      </div>
      <div class=\"card\" id=\"contact\">
        <h2>Limited Offer</h2>
        <p>One-time setup: $997. No monthly maintenance required.</p>
        <a class=\"btn\" href=\"{{ pricing_link }}\">View Pricing & Checkout</a>
      </div>
    </main>
  </body>
</html>
"""
)


def create_demo_page(
    business: Business,
    *,
    pricing_link: str,
    output_dir: str = "data/demos",
) -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    filename = f"{business.place_id}.html"
    destination = path / filename
    destination.write_text(
        DEMO_TEMPLATE.render(business=business, pricing_link=pricing_link),
        encoding="utf-8",
    )
    return destination
