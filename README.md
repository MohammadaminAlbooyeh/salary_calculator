# Salary Calculator

A simple Flask-based salary calculator.

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```

2. Run the app:
   ```bash
   python backend/main.py
   ```

3. Test the API:
   ```bash
   curl -X POST http://localhost:5000/calculate -H "Content-Type: application/json" -d '{"base_salary": 50000, "bonus": 5000, "deductions": 2000}'
   ```

## Docker image

Build the Docker image:
```bash
docker build -t salary_calculator:latest .
```

Run the containerized API locally (example using host port 5000):
```bash
# run with container PORT set to 5000
docker run --rm --name salary_calc -e PORT=5000 -p 5000:5000 salary_calculator:latest
```

Or use the default `PORT=10000` from the Dockerfile:
```bash
docker run --rm --name salary_calc -p 10000:10000 salary_calculator:latest
```

Health-check (wait a few seconds after starting, then):
```bash
curl -v http://localhost:5000/ || curl -v http://localhost:10000/
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