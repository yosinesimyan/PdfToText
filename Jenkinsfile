pipeline {
  environment {
    //add params for Docker Image Name and Last Docker Image Name. we will use them later.
    dockerimagename = "yosinesimyan/pdftotext:1.${BUILD_NUMBER}"
    lastdockerimagename = "yosinesimyan/pdftotext:1.${BUILD_NUMBER-1}"
    dockerImage = ""
   

        //Just another way to use jenkins credentials:
        //CREDS = credentials('Mysql-Credentials')
        //steps {
        // username as $CREDS_USR
        // and password as $CREDS_PSW}
  }
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout your code from version control
                git 'https://github.com/yosinesimyan/PdfToText.git'
            }
        }

        stage('Get UserName Password') {   
            steps {   
               script {      
                   withCredentials([usernamePassword(credentialsId: 'Mysql-Credentials', passwordVariable: 'MYSQL_PASSWORD', usernameVariable: 'MYSQL_USER')]) {
                      docker_args = "--build-arg MYSQL_USER=$MYSQL_USER --build-arg MYSQL_PASSWORD=$MYSQL_PASSWORD" 
                  }
               }
            }
        }

        stage('Build image') {
           // when {
                //branch "master"
           //      expression { env.BRANCH_NAME == 'master' }
          //  }
            steps {
                echo "Running ${BUILD_NUMBER} on ${env.JENKINS_URL}"
                //build the docker image that the app will use. 
                script {
                    dir("app"){
                        dockerImage = docker.build docker_args dockerimagename
                    }
                }
            }
        }    
       
     //   stage('Build features image') {
     //       when {
     //           //branch "files"
     //            expression { env.BRANCH_NAME == 'files' }
    //        }
     //       steps {               
     //           withEnv([dockerimagename = "yosinesimyan/pdftotextfeat:1.${BUILD_NUMBER}"]) {
     //                echo "Running ${dockerimagename } on ${env.JENKINS_URL}"
     //                //build the docker image that the app use.                 
     //                script {
     //                    dir("app") {
     //                    sh 'cat Dockerfile'
     //                    dockerImage = docker.build ${docker_args} dockerimagename
     //                    }
     //                }
     //           }
     //            
      //      }
       // }       

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
        stage('Clear Old Docker image') {
           steps {
               script { 
                 //after the new image is ready, we stop and remove the old running docker image                
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