FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV APP_MODE=api
ENV PORT=10000

WORKDIR /app

# Install dependencies (use backend's requirements which include gunicorn)
COPY backend/requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
	&& pip install --no-cache-dir -r requirements.txt \
	&& pip install --no-cache-dir setuptools==65.5.0

# Copy backend code
COPY backend/ .

# Expose port
EXPOSE $PORT

# Run Flask app with gunicorn using the configured PORT
# Use shell form to allow environment variable expansion
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT} main:app"]