pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout your code from version control
                git 'https://github.com/yosinesimyan/PdfToText.git'
            }
        }
       
        stage('Build Docker Image') {
            steps {
                script {
                     // Build the Docker image
                     dir("app"){
                            sh 'docker build -t pyapp:latest .'
                     }
                }
            }
        }
        stage('Clear Old Docker image') {
           steps {
               script {
                 
                 sh 'docker ps -aq --filter="name=WebServer" | xargs docker stop | xargs docker rm'
               }
           }              

        }

        stage('Run Docker Container') {
            steps {
                // Run the Docker container (adjust options as needed)
                //sh 'docker run --rm pyapp:latest'
                sh 'docker run -d -p 5000:5000 --name WebServer pyapp:latest'
            }
        }
    }
    
    post {

        always {
            // Clean up, remove any images or containers if necessary
            sh 'docker rmi pyapp:latest || true'
        }
    }
}

