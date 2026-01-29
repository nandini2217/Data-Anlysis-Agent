from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
import plotly.io as pio
import os

def export_pdf(kpis, summary, charts):
    file_path = "outputs/dashboard.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>AI Business Dashboard</b>", styles["Title"]))
    elements.append(Paragraph(summary, styles["Normal"]))

    table_data = [[k, str(v)] for k, v in kpis.items()]
    elements.append(Table(table_data))

    img_files = []
    for i, fig in enumerate(charts[:4]):
        img = f"outputs/chart_{i}.png"
        pio.write_image(fig, img, width=500, height=350)
        img_files.append(img)
        elements.append(Image(img, width=400, height=280))

    doc.build(elements)

    for img in img_files:
        os.remove(img)

    return file_path
