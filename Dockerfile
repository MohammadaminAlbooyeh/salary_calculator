FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV APP_MODE=api

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Expose Flask port
EXPOSE 5000

# Default: run the Flask API
CMD ["python", "main.py"]