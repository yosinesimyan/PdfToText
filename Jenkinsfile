<<<<<<< HEAD
pipeline {
  environment {
    dockerimagename = "yosinesimyan/pdftotext:1.${BUILD_NUMBER}"
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
                echo "Running ${BUILD_NUMBER} on ${env.JENKINS_URL}"
                //build the docker image that the app use. 
                script {
                    dir("app"){
                        dockerImage = docker.build dockerimagename
                    }
                }
            }
        }       
        stage('Build features image') {
            when {
                branch "files"
            }
            steps {
                dockerimagename = "yosinesimyan/pdftotextfeat:1.${BUILD_NUMBER}"
                echo "Running ${BUILD_NUMBER} on ${env.JENKINS_URL}"
                //build the docker image that the app use. 
                sh 'cat Dockerfile'
                script {
                    dir("app") {
                        dockerImage = docker.build dockerimagename
                    }
                }
            }
        }       

        stage('Pushing Image') {
            environment {
                registryCredential = 'dockerhub-credentials'
                }
            steps {
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
                sh 'docker run -d -p 5000:5000 --name WebServer ${dockerimagename}'
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

=======
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
                sh 'docker run -d -p 5000:5000 pyapp:latest'
            }
        }
    }
    
    post {
        changed {
            script {
                if (currentBuild.currentResult == 'FAILURE') { 
                    emailext subject: '$DEFAULT_SUBJECT',
                        body: '$DEFAULT_CONTENT',
                        recipientProviders: [
                            [$class: 'CulpritsRecipientProvider'],
                            [$class: 'DevelopersRecipientProvider'],
                            [$class: 'RequesterRecipientProvider'] 
                        ], 
                        replyTo: '$DEFAULT_REPLYTO',
                        to: '$DEFAULT_RECIPIENTS'
                }
            }

        always {
            // Clean up, remove any images or containers if necessary
            sh 'docker rmi pdftotext:latest || true'
        }
    }
}

>>>>>>> ef21f745f3c60dd7a429e728f6531772b33004bd
