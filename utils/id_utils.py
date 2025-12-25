def normalize_uid(uid: str) -> str:
    """
    Normalize RFID UID for consistency.
    """
    return uid.strip().upper()


def normalize_device_id(device_id: str) -> str:
    """
    Normalize device IDs.
    """
    return device_id.strip().upper()
