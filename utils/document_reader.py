from PyPDF2 import PdfReader
import docx

def extract_text(files):
    full_text = ""

    for file in files:
        if file.name.endswith(".pdf"):
            reader = PdfReader(file)
            for page in reader.pages:
                full_text += page.extract_text()

        elif file.name.endswith(".docx"):
            doc = docx.Document(file)
            for p in doc.paragraphs:
                full_text += p.text + "\n"

        elif file.name.endswith(".txt"):
            full_text += file.read().decode("utf-8")

    return full_text
