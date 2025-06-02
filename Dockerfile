# Etap 1: Python slim
FROM python:3.11-slim

# Ustawienia środowiska
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Katalog roboczy
WORKDIR /app

# Kopiujemy pliki projektu
COPY . .

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Zbieranie statycznych plików (z Reacta i admina)
RUN python manage.py collectstatic --noinput

# Uruchomienie serwera deweloperskiego
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

