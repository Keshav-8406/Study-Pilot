import json
import os
from Reminder import send_daily_nudge
from dotenv import load_dotenv

load_dotenv()

def main():
    with open("Timetable.json", "r") as f:
        data = json.load(f)

    rows = []
    for day in data["timetable"]:
        for slot in day["slots"]:
            rows.append({
                "date": day["date"],
                "subject": slot["subject"],
                "topic": ", ".join(slot["chapters_to_cover"]),
                "minutes": slot["duration_minutes"],
                "notes": slot.get("notes", "")
            })

    recipient = os.getenv("Receiver_GMAIL_ID")
    send_daily_nudge(rows, recipient_email=recipient, pdf_path="Timetable.pdf")

if __name__ == "__main__":
    main()