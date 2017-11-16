from django.conf.urls import url

from crawler import views


urlpatterns = [
    url(r"^upload_pdf_file/$", views.upload_pdf_file, name="upload_pdf_file"),
    url(r"^pdf_document/$", views.pdf_document, name="pdf_document"),
    url(r"^create_pdf_document/$", views.pdf_document,
        name="create_pdf_document"),
    url(r"^pdf_document/(?P<pk>\d+)/$", views.pdf_urls, name="pdf_urls"),
    url(r"^url/$", views.urls, name="urls"),
]
