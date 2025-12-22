from datetime import datetime

def entry_message(student_name: str, time: datetime, device: str) -> str:
    return (
        f"📘 Attendance Update\n\n"
        f"{student_name} has ENTERED the school.\n\n"
        f"🕒 Time: {time.strftime('%I:%M %p')}\n"
        f"📍 Gate: {device}\n\n"
        f"– School Attendance System"
    )


def exit_message(student_name: str, time: datetime, device: str) -> str:
    return (
        f"📕 Attendance Update\n\n"
        f"{student_name} has EXITED the school.\n\n"
        f"🕒 Time: {time.strftime('%I:%M %p')}\n"
        f"📍 Gate: {device}\n\n"
        f"– School Attendance System"
    )
