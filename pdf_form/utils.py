from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.acroform import AcroForm
from PyPDF2 import PdfReader, PdfWriter
import io

def make_editable_float_plan(input_pdf, output_pdf):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    form = AcroForm(c)

    # Add form fields
        # Adding form fields
    form.textfield(name="departing_date", x=410, y=497, width=180, height=13, tooltip="Enter Departing Date/Time")
    form.textfield(name="returning_time", x=390, y=482, width=200, height=13, tooltip="Enter Returning Time")
    form.textfield(name="member_name", x=1100, y=460, width=200, height=15, tooltip="Enter Member's Name")
    form.textfield(name="emergency_contact", x=130, y=430, width=150, height=15, tooltip="Enter Emergency Contact")
    form.textfield(name="contact_number", x=390, y=430, width=150, height=15, tooltip="Enter Emergency Contact Number")

    form.textfield(name="signature", x=60, y=80, width=300, height=30, tooltip="Enter Signature")
    form.textfield(name="guest1", x=18, y=400, width=230, height=12, tooltip="Enter guest 1")
    form.textfield(name="guest2", x=18, y=387, width=230, height=12, tooltip="Enter guest 2")
    form.textfield(name="guest3", x=18, y=374, width=230, height=12, tooltip="Enter guest 3")
    form.textfield(name="guest4", x=18, y=361, width=230, height=12, tooltip="Enter guest 4")
    form.textfield(name="guest5", x=18, y=348, width=230, height=12, tooltip="Enter guest 5")
    form.textfield(name="guest6", x=18, y=335, width=230, height=12, tooltip="Enter guest 6")
    form.textfield(name="guest7", x=18, y=322, width=230, height=12, tooltip="Enter guest 7")
    
    
    form.textfield(name="guest8", x=308, y=400, width=230, height=12, tooltip="Enter guest 8")
    form.textfield(name="guest9", x=308, y=387, width=230, height=12, tooltip="Enter guest 9")
    form.textfield(name="guest10", x=308, y=374, width=230, height=12, tooltip="Enter guest 10")
    form.textfield(name="guest11", x=308, y=361, width=230, height=12, tooltip="Enter guest 11")
    form.textfield(name="guest12", x=308, y=348, width=230, height=12, tooltip="Enter guest 12")
    form.textfield(name="guest13", x=308, y=335, width=230, height=12, tooltip="Enter guest 13")
    form.textfield(name="guest14", x=308, y=322, width=230, height=12, tooltip="Enter guest 14")

    c.setFont("Helvetica", 10)
    # c.drawString(50, 690, "Depart Time:")
    # c.drawString(50, 650, "Return Time:")
    # c.drawString(50, 610, "Member Name:")
    # c.drawString(50, 530, "Emergency Number:")
    # c.drawString(50, 490, "Emergency Contact:")
    c.drawString(370, 100, "Member Signature")

    c.save()
    packet.seek(0)

    # Merge form fields with the original PDF
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    new_pdf = PdfReader(packet)

    for i, page in enumerate(reader.pages):
        if i == 0:  # Add form fields to the first page only
            page.merge_page(new_pdf.pages[0])
        writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('usage: python pdf utils.py <input_pd> <output_pdf>')
    else:
        input_pdf = sys.argv[1]
        output_pdf = sys.argv[2]
        make_editable_float_plan(input_pdf,output_pdf)