from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'device_id', 'image_binary', 'created_at')
