FROM python:3.7

EXPOSE 8080

RUN mkdir /yuz

COPY . ./yuz

WORKDIR /yuz/yuz

RUN pip install --no-cache-dir -r requirements.txt && python manage.py collectstatic && pip install uwsgi

ENTRYPOINT ["uwsgi", "--http", ":8080", "--static-map", "/static=./static", "--module", "yuz.wsgi"]