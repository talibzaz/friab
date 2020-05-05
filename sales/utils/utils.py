import os
from django.template.loader import render_to_string

from weasyprint import HTML


# CREATES PDF FILE OF THE GIVEN HTML CODE AND RETURNS LOCATION OF THE CREATED PDF..
def save_pdf(request, html, pdf_path, today, name, id):
    path = pdf_path+"{date}".format(date=today.strftime("%d-%B-%y"))

    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(path):
        f = open(os.path.join(path, '{name}_{id}.pdf'.format(
            name=name.replace(" ", "_"),
            id=id
        )), 'wb')
        f.write(HTML(string=html, base_url=request.build_absolute_uri()).write_pdf())
    return f.name
