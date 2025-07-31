FROM python:3.9.13-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5005

CMD ["sh", "-c", "rasa run actions & rasa run --enable-api --cors '*' --port 10000 --host 0.0.0.0 --endpoints endpoints.yml --connector socketio"]
