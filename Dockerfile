FROM python:3.9-slim-buster

RUN apt-get update \
    && apt-get install -y libpq-dev gcc

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



