PDF Crawler
===========

PDF processing web system. A PDF file is uploaded to the server where the
text is scanned for url links. The url links are saved to the database. The
following REST API handlers are used to upload and requests data.

- `/crawler/upload_pdf_file/` to upload a PDF document
- `/crawler/pdf_document/` request a list of uploaded PDF documents
- `/crawler/pdf_document/[id]/` to get urls for a specific document
- `/crawler/url/` to get all urls with the number of PDF files, containing it

To test the service we can use `curl`. To test file upload.

`curl -F "name=pdfdoc" -F "pdf=@file.pdf" http://localhost:8000/crawler/upload_pdf_file/`

To test a request for document list.

`curl http://localhost:8000/crawler/pdf_document/`

To test a request for urls in one document.

`curl http://localhost:8000/crawler/pdf_document/[id]/`

To test a request for all urls.

`curl http://localhost:8000/crawler/url/`

Visit `/crawler/upload_pdf_file/` to manually add urls from a PDF file.
