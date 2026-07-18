from __future__ import annotations

import html
import resend
from flask import current_app


def configured() -> bool:
    return bool(current_app.config.get("RESEND_API_KEY") and (current_app.config.get("RESEND_TO_EMAIL") or current_app.config.get("CONTACT_TO_EMAIL")))


def send_contact_email(name: str, sender_email: str, subject: str, message: str) -> str | None:
    if not configured():
        return None

    resend.api_key = current_app.config["RESEND_API_KEY"]
    recipient = current_app.config.get("RESEND_TO_EMAIL") or current_app.config.get("CONTACT_TO_EMAIL") or ""
    safe_name = html.escape(name)
    safe_email = html.escape(sender_email)
    safe_subject = html.escape(subject or "Pesan dari Portofolio")
    safe_message = html.escape(message).replace("\n", "<br>")

    response = resend.Emails.send(
        {
            "from": current_app.config["RESEND_FROM_EMAIL"],
            "to": [recipient],
            "reply_to": sender_email,
            "subject": f"Portofolio Vanessa: {subject or 'Pesan baru'}",
            "html": f"""
                <h2>Pesan baru dari website portofolio</h2>
                <p><strong>Nama:</strong> {safe_name}</p>
                <p><strong>Email:</strong> {safe_email}</p>
                <p><strong>Subjek:</strong> {safe_subject}</p>
                <p><strong>Pesan:</strong><br>{safe_message}</p>
            """,
        }
    )
    return response.get("id") if isinstance(response, dict) else None
