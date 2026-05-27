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

# Cria migrations e banco SQLite na inicializacao
RUN python manage.py migrate --settings=ceres_core.settings_notebook --run-syncdb 2>/dev/null || true

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080", \
     "--settings=ceres_core.settings_notebook", \
     "--noreload", "--nothreading"]
