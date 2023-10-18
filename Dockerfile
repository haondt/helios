FROM python:3.11.1-alpine

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY ./app ./app
COPY ./server.py .

ENTRYPOINT ["gunicorn", "-w", "2", "-b", "0.0.0.0", "server:helios"]

