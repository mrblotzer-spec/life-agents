from dataclasses import dataclass
import os


@dataclass
class Settings:
    google_maps_api_key: str
    twilio_account_sid: str | None = None
    twilio_auth_token: str | None = None
    twilio_phone_number: str | None = None
    stripe_api_key: str | None = None
    stripe_price_link: str | None = None
    output_dir: str = "data"



def load_settings() -> Settings:
    return Settings(
        google_maps_api_key=os.environ["GOOGLE_MAPS_API_KEY"],
        twilio_account_sid=os.environ.get("TWILIO_ACCOUNT_SID"),
        twilio_auth_token=os.environ.get("TWILIO_AUTH_TOKEN"),
        twilio_phone_number=os.environ.get("TWILIO_PHONE_NUMBER"),
        stripe_api_key=os.environ.get("STRIPE_API_KEY"),
        stripe_price_link=os.environ.get("STRIPE_PRICE_LINK"),
        output_dir=os.environ.get("OUTPUT_DIR", "data"),
    )
