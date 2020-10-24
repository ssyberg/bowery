from background_task.models import Task
from background_task import background
from .models import Image
import threading
import time

def throttle():
    time.sleep(2)

# Glossing over A LOT here, but this should take about
# 0.75 seconds to run
def s3uploadstub(img_data):
    time.sleep(0.05)
    return True

@background(schedule=1)
def upload_images():
    
    # Get the next 15 images
    images = Image.objects.order_by('id')[:15]
    
    while len(images) > 0:

        # this will guarantee we never move more than 15 images/sec
        throttler = threading.Thread(target=throttle)
        throttler.start()

        for img in images:

            # If upload is successful delete the image
            # if upload fails this will get attempted again on the
            # next go round
            if (s3uploadstub(img)):
                img.delete()

        # get the next set of images
        images = Image.objects.order_by('id')[:15]

        # now see if a second has passed yet
        throttler.join()
