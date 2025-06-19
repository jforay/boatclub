from django.http import FileResponse
from django.shortcuts import render
from .utils import make_editable_float_plan

def float_plan_view(request,):
    pdf_path = "pdf_form/static/pdf_form/Float_plan_fillable.pdf"
    return render(request, )

def upload_filled_plan(request):
    if request.method == "POST" and 'completed_pdf' in request.FILES:
        completed_pdf = request.FILES['completed_pdf']
        # Process or save the completed PDF
        with open(f"path/to/completed/{completed_pdf.name}", "wb") as f:
            for chunk in completed_pdf.chunks():
                f.write(chunk)
        return render(request, "floatplans/success.html", {"message": "Float plan submitted successfully!"})
    return render(request, "floatplans/upload.html")
