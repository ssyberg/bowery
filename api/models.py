from django.db import models

class Image(models.Model):

    device_id = models.TextField(null=False)

    # Note I consider this a huge design flaw - I'm only doing
    # this due to time constraints for the project, normally
    # this would be a file system path with a unique file name
    image_binary = models.BinaryField(null=False)

    created_at = models.DateTimeField(auto_now_add=True)