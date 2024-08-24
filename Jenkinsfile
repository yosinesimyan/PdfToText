pipeline {
  environment {
    //add params for Docker Image Name and Last Docker Image Name. we will use them later.
    dockerimagename = "yosinesimyan/pdftotext:1.${BUILD_NUMBER}"
    dockerimagenamefeat = "yosinesimyan/pdftotextfeat:1.${BUILD_NUMBER}"
    lastdockerimagename = "yosinesimyan/pdftotext:1.${BUILD_NUMBER-1}"
    dockerImage = ""
  }
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout your code from version control
                git 'https://github.com/yosinesimyan/PdfToText.git'
            }
        }
        stage('Build image') {
            when {
                branch "master"
            }
            steps {
                echo "Running ${dockerimagename} on ${env.JENKINS_URL}"
                //build the docker image that the app will use. 
                script {
                    dir("app"){
                        echo "on branch Master"
                        sh 'cat Dockerfile'
                        dockerImage = docker.build(dockerimagename)
                    }
                }
            }
        }       
        stage('Build features image') {
            when {
                branch "files"
            }
            steps {
                echo "Running ${dockerimagenamefeat} on ${env.JENKINS_URL}"
                //build the docker image that the app use.                 
                script {
                    dir("app") {
                        echo "on branch Files"
                        //sh 'cat Dockerfile'
                        dockerImage = docker.build(dockerimagenamefeat)
                    }
                }
            }
        }       

        stage('Pushing Image') {
            environment {
                registryCredential = 'dockerhub-credentials'
                }
            steps {
                //push the image to DockeHub repository
                script {
                   docker.withRegistry( 'https://registry.hub.docker.com', registryCredential ) {
                       dockerImage.push("1.${BUILD_NUMBER}")
                   }
                }
            }
        }        
       // stage('Clear Old Docker image') {
       //    steps {
       //        script { 
       //          //after the new image is ready, we stop and remove the old running docker image                
       //          sh 'docker ps -aq --filter="name=WebServer" | xargs docker stop 2>/dev/null  | xargs docker rm 2>/dev/null || true'
       //        }
       //    }              
       // }

        stage('Run Docker Container') {
            steps {
                echo "Running Docker ${dockerimagename}"
                // Run the Docker container (adjust options as needed)
                dir("app") {
                   withCredentials([usernamePassword(credentialsId: 'Mysql-Credentials', passwordVariable: 'MYSQL_PASSWORD', usernameVariable: 'MYSQL_USER')]) {
                       // f = new File('.env')
                       // f.append('echo MYSQL_USER=$MYSQL_USER')
                       // f.append('\nMYSQL_PASSWORD=$MYSQL_PASSWORD')
                       sh 'echo "MYSQL_USER=$MYSQL_USER" > .env'
                       sh 'echo "MYSQL_PASSWORD=$MYSQL_PASSWORD" >> "\n" >> .env'
                        //sh 'docker run -d -p 5000:5000 --name WebServer ${dockerimagename}'
                       sh 'docker compose up'
                   }
                }
            }
        }
    }
    
    post {
        always {
            echo "Removing Docker image ${lastdockerimagename}"
            // Clean up, remove any images or containers if necessary
            sh 'docker rmi ${lastdockerimagename} || true'
        }
    }
}