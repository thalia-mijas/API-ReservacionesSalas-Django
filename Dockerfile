FROM python:3.13.2-slim-bullseye

EXPOSE 80

COPY . /code

#esto lo realizo porque cree este archivo para migrar de SQLITE a MYSQL
COPY data.json /code/data.json 

WORKDIR /code

RUN apt update
RUN apt upgrade -y
RUN apt install python3-dev default-libmysqlclient-dev build-essential pkg-config nginx -y
RUN pip install -r requirements.txt

RUN python manage.py collectstatic

COPY nginx.conf /etc/nginx/sites-available/default

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

CMD ["bash", "-c", "/wait-for-it.sh mysql-reservas:3306 -- \
    python manage.py migrate && \
    python manage.py loaddata data.json && \
    python manage.py collectstatic && \
    service nginx start && \
    gunicorn reservationsapi.wsgi:application"]