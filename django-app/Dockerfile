FROM alpine:3.4
MAINTAINER Menangen <menangen@gmail.com>

RUN apk --update --no-cache add python-dev py-pip gcc musl-dev postgresql-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY manage.py /usr/src/app
COPY db.sqlite3 /usr/src/app

COPY booking/migrations/*.py /usr/src/app/booking/migrations/

COPY booking/*.py /usr/src/app/booking/

COPY booking/templates/*.html /usr/src/app/booking/templates/
COPY booking/static/dist/ /usr/src/app/booking/static/dist/

COPY travel_booking/*.py /usr/src/app/travel_booking/

COPY manage.py /usr/src/app

EXPOSE 8000
# CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
CMD ["gunicorn", "-w 3", "-b 0.0.0.0:8000", "travel_booking.wsgi"]