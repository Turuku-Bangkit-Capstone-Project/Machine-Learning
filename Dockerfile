# Gunakan image Python sebagai base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Salin requirements.txt dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin kode aplikasi
COPY . .

# Tentukan perintah untuk menjalankan aplikasi
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]