  FROM python:3.9-slim
  expose 5000
  WORKDIR /app
  COPY app.py /app
  COPY templates/ /app
  COPY requirements.txt /app
  #RUN apt-get update && apt-get install -y libpq-dev build-essential
  RUN pip install --no-cache-dir -r requirements.txt
   # ENTRYPOINT ["python" ]

  # CMD ["app.py" ]
  CMD ["python", "app.py"]  # Replace with your entry point

