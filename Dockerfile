FROM python:3

ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

# Wait for it!
RUN chmod +x wait-for-it.sh
RUN chmod +x docker-entrypoint.sh