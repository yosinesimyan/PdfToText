  FROM python:3.9-slim
  WORKDIR /app
  COPY . .
  #RUN apt-get update && apt-get install -y libpq-dev build-essential
  RUN pip install --no-cache-dir -r requirements.txt
 
  CMD ["python", "app.py"]  # Replace with your entry point

