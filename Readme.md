**General Approach**

Due to significant time constraints (not just the 4 hour constraint, but my own availability right now), I chose Python/Django mostly because I had a docker container ready to go (I developed it for another interview take home project) and it's fresh in my head - I make no assertions about it's real world suitability for this particular problem. Of course this choice of framework had bigger implications on what kind of throttling algorithm I could feasibly do with available libraries in 4 hours.

**Upload Throttling Algorithm**

My initial approach was to look for a django s3 library with built in upload rate limiting (in retrospect I should have looked for this library in any language/framework and chose my language based on such a library existing... if it does). It quickly became clear there was no such lib and I would have to essentially roll my own. I briefly considered trying to do this at the socket level, but after a little research it also appeared there was no rate limiting support for python socket packages. I could have gone deeper and attempted to do this at the TCP packet level, monitoring number of packets being sent and sleeping as necessary but figured that would take me far longer than 4 hours to figure out.

I settled on a pretty simple algorithm that has a big flaw (see below). I did some simple math in a spreadsheet (https://docs.google.com/spreadsheets/d/1JoPevP-sIats9GzCZHvxXke-wl41OJqxsp1zgbb8MJc/edit?usp=sharing) and determined we could send about 15 images/second to maintain 50% bandwidth usage. I then spawned a thread that sleeps for one second, used a simple upload loop that uploads 15 photos, and then waits for the spawned thread to finish. 

This is all managed my a background task lib that ended up being a little broken (also discussed a bit below).

**The Big Flaw / Caveat on Performance**

The algorithm I developed guarantees it never exceeds the bandwidth limitation, but it does nothing to guarantee a minimum rate of transfer (though this wasn't explicitly required in the assignment, it's a fair assumption that it's important). Since I was only able to really test this in a local container with dummy data I have some concerns that this would actually be too slow instead of too fast and we could end up with an infinite backlog of images to upload - I’d want to do some testing in a production environment to actually watch how long things were taking and find ways to adjust if necessary.

**Known Issues / Changes I Would Like to Make** 
(my list of changes I would make if I had more time)

- Would not store image binaries in the db
  - I also think images coming in via a json put/post would need to be base64 encoded with would have the effect of increasing the actual file size, not an issue on upload I don’t think but we’d need to take this into account when moving to S3
- As a corollary to the above, I think it would make sense to batch and compress uploads in to packets of some optimal size
- Would implement token authentication and not leave the API wide open
- Would constrain the API endpoints to only those supported (including the HTTP methods)
- Would use celery instead of django-background-tasks but requires more setup
- Currently lacking a way to restart the background process if it ever fails
  - Would use something like cron for managing the background process (or something more robust like supervisor)
- Would not hardcode the throttling variables but would make them easily accessible “settings” in the code -- throttling is currently dependent the throttle threads sleep time and number of images processed per throttle period
- Would add logging/monitoring to make sure upload process was working as expected, backlog wasn’t getting too big, looking for consistent upload failures
- Would actually implement s3 uploads using the django-storages lib - note I installed this in the requirements.txt but spent some time researching and realized stubbing it out would take just as much time as just doing it
- Would add some unit/integration test coverage

**Known Bugs**

- There appears to be a bug in the background tasks lib that was failing to start the background task processing at app startups so my instructions below include starting it by hand

**Setup and "testing"**

- Clone this github repo

- cd in to the root directory 

- run "docker-compose up"

- In a separate terminal run "docker-compose run web bash"

- In the terminal run "python manage.py shell"

- Once on the django shell we'll first verify there are 5000 dummy images in the system, then we'll start the background uploading by calling upload_images() - this only needs to be called once and will now presumable run indefinitely 

  ```
  >>> from api.models import Image
  >>> Image.objects.all().count()
  5000
  >>> from api.tasks import upload_images
  >>> upload_images(repeat=60,repeat_until=None)
  ```
  
  You can then keep running count() to watch the images get processed
  
  ```
  >>> Image.objects.all().count()
  4985
  >>> Image.objects.all().count()
  4980
  >>> Image.objects.all().count()
  4955
  ```
  
  

The API endpoint is also now available at localhost:8000