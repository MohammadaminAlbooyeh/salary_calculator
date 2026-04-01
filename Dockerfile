FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV APP_MODE=api

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Expose Flask/gunicorn port
EXPOSE 5000

# Run with gunicorn for production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]