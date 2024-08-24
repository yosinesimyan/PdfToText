  #It will use python image as the parent image for
  #building the Docker image
  
  FROM python:3.9.19-slim-bullseye

  #create a working directory for the Python app
  #the python app will run from this working directory.
 
  WORKDIR /app

  #Copy the python application files from the 
  #repository to the python app working directory.
  
  COPY . . 
  
  RUN apt-get update && apt-get upgrade -y
  RUN apt-get install -y gcc default-libmysqlclient-dev pkg-config \
  && rm -rf /var/lib/apt/lists/*

  #install all the python application dependencies  
  RUN pip install --no-cache-dir -r requirements.txt
  
  CMD ["python", "app.py"]  # entry point

