import os
import sys

from docxtpl import DocxTemplate

from certificate.models import GeneratedDocument
from tags.tag_manager import manager


def gen_document(document_id):
    document = GeneratedDocument.objects.get(id=document_id)
    demand = document.demand
    document_template = demand.file
    output_filename = "output.docx"

    basedir = os.path.dirname(sys.argv[0])
    path = document_template.path
    outpath = os.path.join(basedir, "", output_filename)

    warnings = set()

    template = DocxTemplate(path)
    document.save()
    context = {}
    for tag_name, tag in manager.get_tags().items():
        tmp = tag(profile=document.author, course=document.demand.course, id=document.id)
        context[tag.name] = tmp.get_data()

    template.render(context)
    template.save(outpath)
    document.set_document(outpath, 'Сертификат.docx')
    document.save()
