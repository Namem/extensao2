FROM python:3.12-slim

WORKDIR /app

# Dependencias de sistema para Pillow e TFLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-backend.txt .
RUN pip install --no-cache-dir -r requirements-backend.txt

COPY . .

EXPOSE 8080

ENV PYTHONUNBUFFERED=1

ENV DJANGO_SETTINGS_MODULE=ceres_core.settings_railway

CMD ["sh", "-c", \
     "python manage.py migrate --run-syncdb 2>/dev/null || true && \
      python manage.py popular_teste 2>/dev/null || true && \
      python manage.py mqtt_listener \
        --host ${CERES_BROKER:-localhost} --port ${MQTT_PORT:-1883} \
        --user ${MQTT_USER:-} --password ${MQTT_PASSWORD:-} \
        ${CERES_TLS:+--tls} ${MQTT_WEBSOCKET:+--websocket} 2>&1 & \
      python manage.py runserver 0.0.0.0:8080 --noreload --nothreading"]
