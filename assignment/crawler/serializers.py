from rest_framework import serializers

from crawler.models import PdfDocument, Url


class PdfDocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PdfDocument
        fields = ("pk", "name", "urls_count")


class UrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Url
        fields = ("url", "status")


class UrlPdfSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    url = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=3)  # HTTP Status Code
    pdf__count = serializers.IntegerField()
