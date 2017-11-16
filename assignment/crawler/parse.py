from cStringIO import StringIO
import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import requests
from requests.exceptions import ConnectionError

from .models import PdfDocument, Url


def get_pdf_text(pdf):
    rsrcmgr = PDFResourceManager()
    buf = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, buf, codec="utf-8", laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(pdf):
        interpreter.process_page(page)

    text = buf.getvalue()

    device.close()
    buf.close()

    return text


def parse_pdf_document(pdf, name):  # TODO: should be an async Celery task
    pt = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|"
                    "(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    pdf_document = PdfDocument.objects.create(name=name)
    text = get_pdf_text(pdf)
    for url in re.findall(pt, text):
        url_instance, created = Url.objects.get_or_create(
            url=url, defaults={"status": ""})
        try:
            response = requests.get(url)
            url_instance.status = str(response.status_code)
            url_instance.save()
        except ConnectionError:
            pass
        url_instance.pdf.add(pdf_document)
