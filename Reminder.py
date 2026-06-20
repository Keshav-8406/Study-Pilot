import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import date
from dotenv import load_dotenv

load_dotenv()


def send_daily_nudge(rows, recipient_email, pdf_path=None):
    today = date.today().isoformat()

    today_tasks = [row for row in rows if row["date"] == today]

    sender_email = os.getenv("GMAIL_ID")
    app_password = os.getenv("GMAIL_Password")

    table_rows = ''.join(
        f"<tr>"
        f"<td>{r['subject']}</td>"
        f"<td>{r['topic']}</td>"
        f"<td>{r['minutes']} min</td>"
        f"<td><i>{r['notes']}</i></td>"
        f"</tr>"
        for r in today_tasks
    )

    total_mins = sum(r['minutes'] for r in today_tasks)

    html = f"""
    <h2>StudyPilot - {today}</h2>

    <table border="1" cellpadding="6">
        <tr>
            <th>Subject</th>
            <th>Topics</th>
            <th>Time</th>
            <th>Notes</th>
        </tr>

        {table_rows}

    </table>

    <p><strong>Total today: {total_mins} minutes</strong></p>

    <p>Stay consistent. See you tomorrow.</p>
    """

    msg = MIMEMultipart('mixed')
    msg['Subject'] = f'StudyPilot - Your plan for {today}'
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.attach(MIMEText(html, 'html'))

    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            part = MIMEApplication(f.read(), _subtype="pdf")
            part.add_header(
                "Content-Disposition", "attachment",
                filename=os.path.basename(pdf_path)
            )
            msg.attach(part)
    elif pdf_path:
        print(f"Warning: pdf_path given but file not found -> {pdf_path}")

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f'Nudge sent to {recipient_email}')