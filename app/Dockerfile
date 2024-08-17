  #It will use python image as the parent image for
  #building the Docker image
  
  ARG MYSQL_USER
  ARG MYSQL_PASSWORD
  
  FROM python:3.9.19-slim-bullseye

  #create a working directory for the Python app
  #the python app will run from this working directory.
 
  WORKDIR /app

  #Copy the python application files from the 
  #repository to the python app working directory.
  
  COPY . . 
  
  # RUN apt-get update && apt-get upgrade
  # RUN apt-get install -y libpq-dev build-essential
  # RUN pip install --upgrade pip
   
    RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*
    RUN pip install --upgrade pip
  

  #install all the python application dependencies

  
  RUN pip install --no-cache-dir -r requirements.txt

  #The command to start the python application container
  RUN --mount=type=secret,id=MYSQL_USER \
      --mount=type=secret,id=MYSQL_PASSWORD \
  echo "MySQL user: $(cat /run/secrets/mysql_user)" 
  CMD ["python", "app.py", $MYSQL_PASSWORD, $MYSQL_PASSWORD]  # entry point

