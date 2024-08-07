pipeline {
  environment {
    dockerimagename = "yosinesimyan/pdftotext"
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
            steps{
                script {
                    dir("app"){
                        dockerImage = docker.build dockerimagename
                    }
                }
            }
        }       
        // stage('Build Docker Image') {
        //     steps {
        //         script {
        //              // Build the Docker image
        //              dir("app"){
        //                     sh 'docker build -t app-web:latest .'
        //              }
        //         }
        //     }
        // }

        stage('Pushing Image') {
            environment {
                registryCredential = 'dockerhub-credentials'
                }
            steps{
                script {
                docker.withRegistry( 'https://registry.hub.docker.com', registryCredential ) {
                    dockerImage.push("latest")
                }
                }
            }
            }        
        stage('Clear Old Docker image') {
           steps {
               script {
                 
                 sh 'docker ps -aq --filter="name=WebServer" | xargs docker stop 2>/dev/null  | xargs docker rm 2>/dev/null || true'
               }
           }              

        }

        stage('Run Docker Container') {
            steps {
                // Run the Docker container (adjust options as needed)
                //sh 'docker run --rm pyapp:latest'
                sh 'docker run -d -p 5000:5000 --name WebServer yosinesimyan/pdftotext'
            }
        }
    }
    
    post {

        always {
            // Clean up, remove any images or containers if necessary
            sh 'docker rmi pdftotext:latest || true'
        }
    }
}

