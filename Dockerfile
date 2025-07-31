FROM python:3.9.13-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["rasa", "run", "--enable-api", "--cors", "*"]
