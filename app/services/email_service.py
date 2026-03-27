import os
import smtplib
from email.mime.text import MIMEText

def send_email(to_address: str, subject: str, body: str) -> bool:
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("EMAIL_FROM") or smtp_username
    if not smtp_host or not sender:
        print(f"[EMAIL_DISABLED] To={to_address} Subject={subject}")
        return False
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_address
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            if smtp_username and smtp_password:
                server.login(smtp_username, smtp_password)
            server.sendmail(sender, [to_address], msg.as_string())
        return True
    except Exception as exc:
        print(f"[EMAIL_ERROR] {exc}")
        return False
