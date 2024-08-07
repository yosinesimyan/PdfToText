pipeline {
  environment {
    dockerimagename = "yosinesimyan/pdftotext:1.${BUILD_NUMBER}"
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
                echo "Running ${BUILD_NUMBER} on ${env.JENKINS_URL}"
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
                    dockerImage.push("1.${BUILD_NUMBER}")
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
                echo "Running Docker ${dockerimagename}"
                // Run the Docker container (adjust options as needed)
                //sh 'docker run --rm pyapp:latest'
                sh 'docker run -d -p 5000:5000 ${dockerimagename}'
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

