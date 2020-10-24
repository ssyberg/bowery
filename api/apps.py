from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        from .tasks import upload_images

        # Start the background task, this should work
        # may be a bug in the library or an incompatiblity with this version
        # of django
        #upload_images(repeat=60,repeat_until=None)
