# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.test import Client, TestCase
from django.urls import reverse
import mock

from .models import PdfDocument, Url
from .parse import parse_pdf_document


class TestCrawler(TestCase):

    def setUp(self):
        self.client = Client()
        self.doc1 = PdfDocument.objects.create(name="document1")
        self.doc2 = PdfDocument.objects.create(name="document2")
        url1 = Url.objects.create(url="https://www.djangoproject.com",
                                  status="200")
        url1.pdf.add(self.doc1)
        url2 = Url.objects.create(url="https://google.com",
                                  status="200")
        url2.pdf.add(self.doc1)

    def test_pdf_document(self):
        response = self.client.get(reverse("crawler:pdf_document"))
        obj = json.loads(response.content)
        self.assertTrue({"pk": 1, "name": "document1", "urls_count": 2} in obj)

    def test_pdf_document_urls(self):
        response = self.client.get(reverse("crawler:pdf_urls",
                                           kwargs={"pk": "1"}))
        obj = json.loads(response.content)
        self.assertTrue({"url": "https://google.com", "status": "200"} in obj)

    def test_pdf_urls(self):
        response = self.client.get(reverse("crawler:urls"))
        obj = json.loads(response.content)
        self.assertTrue({"url": "https://google.com", "pk": 2, "pdf__count": 1,
                         "status": u"200"} in obj)


class TestPdfParse(TestCase):

    def test_parse_pdf_document(self):
        with mock.patch("crawler.parse.get_pdf_text") as get_pdf_text:
            get_pdf_text.return_value = ("line1\nhttp://python.org\nline3\n"
                                         "http://invalid.tld")
            parse_pdf_document(None, "pdfdoc")
            new_doc = PdfDocument.objects.get(name="pdfdoc")
            self.assertEqual(new_doc.name, "pdfdoc")
            new_url = Url.objects.get(url="http://invalid.tld")
            self.assertEqual(new_url.status, "")
