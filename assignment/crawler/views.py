# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import PdfDocument, Url
from .serializers import PdfDocumentSerializer, UrlSerializer, UrlPdfSerializer
from .forms import UploadFileForm
from .parse import parse_pdf_document


@csrf_exempt
def upload_pdf_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            parse_pdf_document(request.FILES["pdf"], form.data["name"])
            return HttpResponse(status=204)
    return HttpResponse(status=404)


def create_pdf_document(request):
    if request.method == "GET":
        form = UploadFileForm()
    elif request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            parse_pdf_document(request.FILES["pdf"], form.data["name"])
            return HttpResponseRedirect(request.path)
    return render(request, "crawler/upload.html", {"form": form})


def pdf_document(request):
    pdf_documents = PdfDocument.objects.all()
    if pdf_documents.exists():
        serializer = PdfDocumentSerializer(pdf_documents, many=True)
        return JsonResponse(serializer.data, safe=False)
    return HttpResponse(status=404)


def pdf_urls(request, pk):
    urls = Url.objects.filter(pdf__pk=int(pk))
    if urls.exists():
        serializer = UrlSerializer(urls, many=True)
        return JsonResponse(serializer.data, safe=False)
    return HttpResponse(status=404)


def urls(request):
    urls = Url.objects.annotate(Count("pdf")).values("pk", "url", "status",
                                                     "pdf__count")
    if urls.exists():
        serializer = UrlPdfSerializer(urls, many=True)
        return JsonResponse(serializer.data, safe=False)
    return HttpResponse(status=404)
