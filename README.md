# Salary Calculator

A simple Flask-based salary calculator.

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```

2. Run the app:
   ```bash
   python src/main.py
   ```

3. Test the API:
   ```bash
   curl -X POST http://localhost:5000/calculate -H "Content-Type: application/json" -d '{"base_salary": 50000, "bonus": 5000, "deductions": 2000}'
   ```

## Docker image

Build the Docker image:
```bash
docker build -t salary-calculator:latest .
```

You can run the Streamlit UI locally in a container:
```bash
docker run --name salary-ui -d -p 8501:8501 salary-calculator:latest
open http://localhost:8501
```

## API Usage

POST /calculate

Request body:
```json
{
  "base_salary": 50000,
  "bonus": 5000,
  "deductions": 2000
}
```

Response:
```json
{
  "total_salary": 53000
}
```