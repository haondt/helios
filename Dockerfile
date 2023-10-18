FROM python:3.11.1-alpine

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY ./app ./app
COPY ./server.py .

CMD ["python3", "-u", "server.py"]
