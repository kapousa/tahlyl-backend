import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http.client import HTTPException


def send_email_with_pdf(email: str, pdf_path: str):
    """Sends an email with the PDF report as an attachment."""
    msg = MIMEMultipart()
    msg['From'] = os.getenv("EMAIL_SENDER")  # your email
    msg['To'] = email
    msg['Subject'] = "Tahlyl | Blood Test Analysis Report"
    body = "Please find your blood test analysis report attached."
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_path, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_path))
        msg.attach(attach)

    try:
        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))  # smtp server and port
        server.starttls()
        server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))  # email and password
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")


def send_analysis_results_email(report_type: str, email: str, analysis_dict: dict, arabic: bool):
    """Sends an email with the analysis results in the body (HTML)."""
    msg = MIMEMultipart()
    msg['From'] = os.getenv("EMAIL_SENDER")
    msg['To'] = email
    msg['Subject'] = f"تقرير تحليل نتائج {report_type}" if arabic else f"{report_type} Analysis Report"

    body = ""
    if arabic:
        body += "<div style=\"direction: rtl; text-align: right;\">"
        body += f"<h2>{'تقرير تحليل نتائج {report_type}:' if arabic else '{report_type} Analysis Report:'}</h2>"

        for key, value in analysis_dict.items():
            if value is not None:
                if key == 'lifestyle_changes' or key == 'diet_routine' or key == 'recommendations' or key == 'key_findings' or key == "potential_causes" or key == "scientific_references" or key == "individualized_recommendations":
                    if isinstance(value, list):
                        body += f"<h3>{key.replace('_', ' ').capitalize()}:</h3><ul>"
                        for item in value:
                            if isinstance(item, dict):
                                for inner_key, inner_value in item.items():
                                    body += f"<li>{inner_key.capitalize()}: {inner_value}</li>"
                            else:
                                body += f"<li>{item}</li>"
                        body += "</ul>"
                    elif isinstance(value, dict):
                        body += f"<h3>{key.replace('_', ' ').capitalize()}:</h3><ul>"
                        for inner_key, inner_value in value.items():
                            if isinstance(inner_value, list):
                                for inner_item in inner_value:
                                    body += f"<li>{inner_key.capitalize()}: {inner_item}</li>"
                            else:
                                body += f"<li>{inner_key.capitalize()}: {inner_value}</li>"
                        body += "</ul>"
                    else:
                        body += f"<p><strong>{key.replace('_', ' ').capitalize()}:</strong> {value}</p>"
                elif isinstance(value, dict):
                    body += f"<h3>{key.replace('_', ' ').capitalize()}:</h3><ul>"
                    for inner_key, inner_value in value.items():
                        if isinstance(inner_value, list):
                            for inner_item in inner_value:
                                body += f"<li>{inner_key.capitalize()}: {inner_item}</li>"
                        else:
                            body += f"<li>{inner_key.capitalize()}: {inner_value}</li>"
                    body += "</ul>"
                else:
                    body += f"<p><strong>{key.replace('_', ' ').capitalize()}:</strong> {value}</p>"

        body += "</div>"
    else:
        body += "<div>"
        body += f"<h2>{report_type} Analysis Report:</h2>"

        for key, value in analysis_dict.items():
            if value is not None:
                if key == 'lifestyle_changes' or key == 'diet_routine' or key == 'recommendations' or key == 'key_findings' or key == "potential_causes" or key == "scientific_references" or key == "individualized_recommendations":
                    if isinstance(value, list):
                        body += f"<h3>{key.replace('_', ' ').capitalize()}:</h3><ul>"
                        for item in value:
                            if isinstance(item, dict):
                                for inner_key, inner_value in item.items():
                                    body += f"<li>{inner_key.capitalize()}: {inner_value}</li>"
                            else:
                                body += f"<li>{item}</li>"
                        body += "</ul>"
                    elif isinstance(value, dict):
                        body += f"<h3>{key.replace('_', ' ').capitalize()}:</h3><ul>"
                        for inner_key, inner_value in value.items():
                            if isinstance(inner_value, list):
                                for inner_item in inner_value:
                                    body += f"<li>{inner_key.capitalize()}: {inner_item}</li>"
                            else:
                                body += f"<li>{inner_key.capitalize()}: {inner_value}</li>"
                        body += "</ul>"
                    else:
                        body += f"<p><strong>{key.replace('_', ' ').capitalize()}:</strong> {value}</p>"
                elif isinstance(value, dict):
                    body += f"<h3>{key.replace('_', ' ').capitalize()}:</h3><ul>"
                    for inner_key, inner_value in value.items():
                        if isinstance(inner_value, list):
                            for inner_item in inner_value:
                                body += f"<li>{inner_key.capitalize()}: {inner_item}</li>"
                        else:
                            body += f"<li>{inner_key.capitalize()}: {inner_value}</li>"
                    body += "</ul>"
                else:
                    body += f"<p><strong>{key.replace('_', ' ').capitalize()}:</strong> {value}</p>"

        body += "</div>"

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
        server.starttls()
        server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")


def send_compare_report_email(email_to: str, body: str, arabic: bool):
    """Sends an email with RTL support for Arabic content."""
    msg = MIMEMultipart()
    msg['From'] = os.getenv('EMAIL_SENDER')
    msg['To'] = email_to
    msg['Subject'] = "Compare Blood Tests Analysis Report"

    if arabic:
        html = f"""
                        <div dir="rtl">
                            {body}
                        </div>
                        """
    else:
        html = f"""
                        <div>
                            {body}
                        </div>
                        """

    msg.attach(MIMEText(html, 'html'))

    try:
        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
        server.starttls()
        server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")
