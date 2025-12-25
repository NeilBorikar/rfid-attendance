def is_valid_attendance_status(status: str) -> bool:
    """
    Check if attendance status is valid.
    """
    return status in {"IN", "OUT"}
