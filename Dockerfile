FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV APP_MODE=streamlit

WORKDIR /app

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY src/ .

# Expose both Flask and Streamlit ports; choose which to run via APP_MODE
EXPOSE 5000 8501

# Default: run Streamlit app. Set APP_MODE=api to run the Flask API instead.
CMD ["sh", "-c", "if [ \"$APP_MODE\" = \"streamlit\" ]; then streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0; else python main.py; fi"]