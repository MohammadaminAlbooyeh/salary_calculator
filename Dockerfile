FROM python:3.11-slim

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV APP_MODE=api
ENV PORT=10000

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Expose port
EXPOSE $PORT

# Run Flask app with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:$PORT", "main:app"]