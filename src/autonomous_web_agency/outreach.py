from __future__ import annotations

from dataclasses import dataclass

from twilio.rest import Client


@dataclass
class OutreachMessage:
    phone_number: str
    body: str


class SmsOutreach:
    """
    Only send to businesses that have explicitly opted in.
    This class intentionally requires opted_in=True to reduce compliance risk.
    """

    def __init__(self, account_sid: str, auth_token: str, from_phone: str):
        self.client = Client(account_sid, auth_token)
        self.from_phone = from_phone

    def send_demo(
        self,
        *,
        to_phone: str,
        business_name: str,
        demo_url: str,
        pricing_url: str,
        opted_in: bool,
    ):
        if not opted_in:
            raise ValueError(
                "Refusing to send SMS without explicit opt-in (TCPA compliance)."
            )

        body = (
            f"Hi {business_name}, we drafted a modern website demo for your business: "
            f"{demo_url}. Pricing and instant checkout: {pricing_url}. "
            "Reply STOP to opt out."
        )
        return self.client.messages.create(
            body=body,
            from_=self.from_phone,
            to=to_phone,
        )
