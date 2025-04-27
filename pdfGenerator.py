from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def split_text(text, length):
    """Helper function to split text into fixed-width lines."""
    return [text[i:i+length] for i in range(0, len(text), length)]

def create_pdf(summary_text):
    """Create a PDF file in memory from the summary text."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    text_object = c.beginText(40, height - 40)
    text_object.setFont("Helvetica", 12)

    for line in summary_text.split('\n'):
        for subline in split_text(line, 90):  # Adjust line length if needed
            text_object.textLine(subline)

    c.drawText(text_object)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
