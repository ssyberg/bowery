from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import ImageSerializer
from .models import Image


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all().order_by('id')
    serializer_class = ImageSerializer

    # Uncomment this in production, leaving get
    # available for testing
    # http_method_names = ['post']