  FROM python:latest 
  #3.9-slim
  WORKDIR /app
  COPY . . 
  # RUN apt-get update && apt-get upgrade
  # RUN apt-get install -y libpq-dev build-essential
  # RUN pip install --upgrade pip
  RUN pip install --no-cache-dir -r requirements.txt
   
  CMD ["python", "app.py"]  # entry point

