FROM python:3.10-slim

WORKDIR app/

COPY requirements.txt .

RUN python3 -m pip install --no-cache -r requirements.txt

COPY . .

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
