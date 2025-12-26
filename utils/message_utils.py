from datetime import datetime


def build_attendance_message(
    student_name: str,
    event_type: str,
    event_time: datetime,
    device: str
) -> str:
    if event_type == "IN":
        return (
            f"📘 Attendance Update\n\n"
            f"{student_name} has ENTERED the school.\n\n"
            f"🕒 Time: {event_time.strftime('%I:%M %p')}\n"
            f"📍 Gate: {device}\n\n"
            f"– School Attendance System"
        )

    if event_type == "OUT":
        return (
            f"📕 Attendance Update\n\n"
            f"{student_name} has EXITED the school.\n\n"
            f"🕒 Time: {event_time.strftime('%I:%M %p')}\n"
            f"📍 Gate: {device}\n\n"
            f"– School Attendance System"
        )

    raise ValueError("Invalid attendance event type")
