def normalize_whatsapp_number(phone: str) -> str:
    """
    Normalize a phone number for WhatsApp messaging.
    Ensures exactly one 'whatsapp:' prefix.
    """
    phone = phone.strip()

    if phone.startswith("whatsapp:"):
        return phone

    return f"whatsapp:{phone}"
