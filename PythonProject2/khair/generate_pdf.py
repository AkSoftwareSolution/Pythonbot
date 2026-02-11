from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf(report, filename="seo_report.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    text = c.beginText(40, 800)
    text.setFont("Helvetica", 10)

    text.textLine("SEO AUDIT REPORT")
    text.textLine("Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    text.textLine("="*60)

    for k, v in report.items():
        text.textLine(f"{k} : {v}")

    c.drawText(text)
    c.save()

