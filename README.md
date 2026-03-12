# life-agents

Autonomous local-business website upgrade pipeline.

## What this does

1. Pulls small-business leads from Google Maps Places API for a target area.
2. Audits each business website and assigns a grade (A-F).
3. Generates demo replacement sites for businesses graded D/F (including no-website businesses).
4. Exports JSON reports for all leads and priority outreach.
5. Includes a compliant SMS outreach helper (requires explicit opt-in before sending).

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
export GOOGLE_MAPS_API_KEY=your_key
# optional
export STRIPE_PRICE_LINK=https://buy.stripe.com/your_link
python -m autonomous_web_agency.main --lat 37.7749 --lng -122.4194 --radius 5000
```

Output:
- `data/report.json`
- `data/demos/<place_id>.html`

## Compliance notes

- Respect Google Maps API Terms and applicable laws.
- Only send SMS to contacts who have explicitly opted in (TCPA and local compliance).
- Keep opt-out language in every outreach message.
