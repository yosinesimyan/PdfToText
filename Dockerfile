  FROM python:3.9-slim
  WORKDIR /app
  COPY . .
  # Install dependencies if you have a requirements.txt
  RUN pip install --no-cache-dir -r requirements.txt
  CMD ["python", "app.py"]  # Replace with your entry point

