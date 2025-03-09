FROM python:3.11-slim

WORKDIR /app

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

COPY templates ./templates
COPY modules ./modules

#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:app"]