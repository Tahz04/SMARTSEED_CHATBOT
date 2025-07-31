FROM python:3.9.13-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN rasa train

CMD sh -c "rasa run --enable-api --cors '*' --port $PORT --host 0.0.0.0 --endpoints endpoints.yml --connector socketio"
