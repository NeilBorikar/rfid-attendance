from datetime import datetime


def build_attendance_message(
    student_name: str,
    event_type: str,
    event_time: datetime,
    location: str
) -> str:
    """
    Build WhatsApp attendance message.
    """
    return (
        "📌 Attendance Update\n\n"
        f"Student: {student_name}\n"
        f"Status: {event_type}\n"
        f"Time: {event_time.strftime('%H:%M:%S')}\n"
        f"Location: {location}"
    )
