FROM python:3.10-alpine
COPY . /mande
EXPOSE 8000
RUN apk update
RUN apk add libpq-dev
RUN apk add build-base
RUN pip3 install -r /mande/requirements.txt
RUN echo "python /mande/manage.py runserver 0.0.0.0:8000" > /runserver.sh 