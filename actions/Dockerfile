FROM python:3.9.13-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["rasa", "run", "actions", "--port", "8000", "--host", "0.0.0.0"]
