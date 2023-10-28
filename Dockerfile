FROM python:3.10-alpine
COPY . /mande
EXPOSE 8000
ENV PORT=8000
RUN apk update
RUN apk add libpq-dev
RUN apk add build-base
WORKDIR /mande
RUN pip3 install -r requirements.txt
RUN python manage.py collectstatic --no-input
CMD ["gunicorn", "mande_backend.wsgi", "--bind", "0.0.0.0:8000"]