# Etap 1: Python slim
FROM python:3.11-slim

# Ustawienia środowiska
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Zmienna środowiskowa do tworzenia superużytkownika
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=admin123

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

# Migracje i statyczne pliki
RUN python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    python manage.py createsuperuser --noinput || true

# Uruchomienie serwera deweloperskiego
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
