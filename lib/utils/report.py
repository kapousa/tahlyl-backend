from reportlab.pdfgen import canvas


def generate_pdf_report(analysis_dict: dict, output_path: str):
    """Generates a PDF report from the analysis results."""
    c = canvas.Canvas(output_path)
    c.drawString(100, 750, "Analysis Report")
    c.drawString(100, 700, f"Summary: {analysis_dict['summary']}")
    c.drawString(100, 650, "Lifestyle Changes:")
    y = 630
    for change in analysis_dict['lifestyle_changes']:
        c.drawString(120, y, f"- {change}")
        y -= 20
    c.drawString(100, y, "Diet Routine:")
    y -= 20
    for routine in analysis_dict['diet_routine']:
        c.drawString(120, y, f"- {routine}")
        y -= 20
    c.save()
