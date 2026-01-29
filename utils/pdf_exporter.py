import pdfkit
import tempfile
import os


def export_dashboard_pdf(html_content):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdfkit.from_string(html_content, tmp.name)
        return tmp.name

