import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_with_pdf(email: str, pdf_path: str):
    """Sends an email with the PDF report as an attachment."""
    msg = MIMEMultipart()
    msg['From'] = os.getenv("EMAIL_SENDER") # your email
    msg['To'] = email
    msg['Subject'] = "Tahlyl | Blood Test Analysis Report"
    body = "Please find your blood test analysis report attached."
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_path, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_path))
        msg.attach(attach)

    try:
        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) # smtp server and port
        server.starttls()
        server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD")) # email and password
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

def send_email_with_results(email: str, analysis_dict: dict, arabic: bool):
    """Sends an email with the analysis results in the body (HTML)."""
    msg = MIMEMultipart()
    msg['From'] = os.getenv("EMAIL_SENDER")
    msg['To'] = email
    msg['Subject'] = "Blood Test Analysis Report"

    if arabic:
        body = f"""
        <div style="direction: rtl; text-align: right;">
            <h2>تقرير تحليل نتائج اختبار الدم:</h2>

            <p><strong>ملخص:</strong> {analysis_dict['summary']}</p>

            <h3>تغييرات نمط الحياة المقترحة:</h3>
            <ul>
        """
        for change in analysis_dict['lifestyle_changes']:
            body += f"<li>{change}</li>"

        body += f"""
            </ul>
            <h3>روتين الحمية المقترح:</h3>
            <ul>
        """
        for routine in analysis_dict['diet_routine']:
            body += f"<li>{routine}</li>"

        body += """
            </ul>
        </div>
        """
    else:
        body = f"""
        <div>
            <h2>Blood Test Analysis Report:</h2>

            <p><strong>Summary:</strong> {analysis_dict['summary']}</p>

            <h3>Suggested Lifestyle Changes:</h3>
            <ul>
        """
        for change in analysis_dict['lifestyle_changes']:
            body += f"<li>{change}</li>"

        body += f"""
            </ul>
            <h3>Suggested Diet Routine:</h3>
            <ul>
        """
        for routine in analysis_dict['diet_routine']:
            body += f"<li>{routine}</li>"

        body += """
            </ul>
        </div>
        """

    msg.attach(MIMEText(body, 'html'))  # Set subtype to 'html'

    try:
        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
        server.starttls()
        server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")
