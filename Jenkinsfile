pipeline {
  environment {
    //add params for Docker Image Name and Last Docker Image Name. we will use them later.
    dockerimagename = "yosinesimyan/pdftotext:1.${BUILD_NUMBER}"
    dockerimagenamefeat = "yosinesimyan/pdftotextfeat:1.${BUILD_NUMBER}"
    lastdockerimagename = "yosinesimyan/pdftotext:1.${BUILD_NUMBER-1}"
    dockerImage = ""
    //AWS_ACCESS_KEY_ID = credentials('aws-creds')
    //AWS_SECRET_ACCESS_KEY = credentials('your-aws-secret-access-key')
    AWS_REGION = 'us-east-1' // Change as needed
    INSTANCE_TYPE = 't2.micro' // Change as needed
    AMI_ID = 'ami-066784287e358dad1' // Replace with a valid AMI ID

  }
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout your code from version control
                git 'https://github.com/yosinesimyan/PdfToText.git'
            }
        }
        stage('Build master image') {
            when {
                branch "master"
            }
            steps {
                echo "Running ${dockerimagename} on ${env.JENKINS_URL}"
                //build the docker image that the app will use. 
                script {
                    dir("app"){
                        dockerImage = docker.build(dockerimagename, "-t yosinesimyan/pdftotext:latest .")
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
                        dockerImage = docker.build(dockerimagenamefeat, "-t yosinesimyan/pdftotextfeat:latest .")
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
                       dockerImage.push("latest")
                   }
                }
            }
        }        
        stage('Create EC2 Instance') {
            steps {
                script {
                    // Create EC2 instance
                    sh('export AWS_PAGER=""')
                    def instanceId = sh(script: '''
                        aws ec2 run-instances --image-id ${AMI_ID} --count 1 --instance-type ${INSTANCE_TYPE} \
                        --key-name your-key-pair-name --query "Instances[0].InstanceId" --output text
                    ''', returnStdout: true).trim()
                    
                    // Wait until the instance is running
                    sh "aws ec2 wait instance-running --instance-ids ${instanceId}"
                    echo "Created EC2 instance: ${instanceId}"
                    
                    // Get the public DNS name of the instance
                    env.INSTANCE_DNS = sh(script: "aws ec2 describe-instances --instance-ids ${instanceId} --query 'Reservations[0].Instances[0].PublicDnsName' --output text", returnStdout: true).trim()
                }
            }
        }
        stage('Deploy Docker on EC2') {
            steps {
                script {
                    // Install Docker on the instance and run the container
                    withCredentials([usernamePassword(credentialsId: 'Mysql-Credentials', passwordVariable: 'MYSQL_PASSWORD', usernameVariable: 'MYSQL_USER')]) {

                        sh """
                        ssh -o StrictHostKeyChecking=no -i /root/.ssh/yosi-kp.pem ec2-user@${INSTANCE_DNS} '
                            sudo yum update -y &&
                            sudo amazon-linux-extras install docker -y &&
                            sudo service docker start &&
                            sudo docker pull ${dockerimagename}:latest &&
                            echo "MYSQL_USER=$MYSQL_USER" > .env &&
                            echo "MYSQL_PASSWORD=$MYSQL_PASSWORD" >> "\n" >> .env &&
                            sudo docker compose up
                        '
                        """
                    }
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                echo "Running Docker ${dockerimagename}"
                // Run the Docker container (adjust options as needed)
                dir("app") {
                   withCredentials([usernamePassword(credentialsId: 'Mysql-Credentials', passwordVariable: 'MYSQL_PASSWORD', usernameVariable: 'MYSQL_USER')]) {
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