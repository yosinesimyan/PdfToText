pipeline {
  environment {
    //add params for Docker Image Name and Last Docker Image Name. we will use them later.
    dockerimagename = "yosinesimyan/pdftotext:1.${BUILD_NUMBER}"
    dockerimagenamefeat = "yosinesimyan/pdftotextfeat:1.${BUILD_NUMBER}"
    lastdockerimagename = "yosinesimyan/pdftotext:1.${BUILD_NUMBER-1}"
    dockerImage = ""
    AWS_REGION = 'us-east-1' // Change as needed
    INSTANCE_TYPE = 't2.micro' // Change as needed
    AMI_ID = 'ami-066784287e358dad1' // Replace with a valid AMI ID\
    AWS_KEYPAIR = "Yosi-KP"

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
                expression {
                             return env.BRANCH_NAME != 'master';
                       }           
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
                       //dockerImage.push("latest")
                   }
                }
            }
        }        
        stage('Create EC2 Instance') {
            when {
                branch "AWS"
            }
            steps {
                script {                                    
                    // Create EC2 instance
                    sh('export AWS_PAGER=""')
                    // define UserData for AWS EC2 Instance pre-build
                    
                    def userDataScript = '''
                        #!/bin/bash                               
                        yum update -y
                        yum install docker -y
                        service docker start
                        systemctl enable docker
                        aws s3 cp s3://firstbucket-yosi/compose.yaml /home/ec2-user/compose.yaml
                        curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                        chmod +x /usr/local/bin/docker-compose
                        '''
                    echo ${userDataScript}
                    
                    // Encode the user data script in Base64
                    def userDataEncoded = userDataScript.bytes.encodeBase64().toString()

                    //Create the AWS EC2 Instance
                    def instanceId = sh(script: '''
                        aws ec2 run-instances --image-id ${AMI_ID} --count 1 --instance-type ${INSTANCE_TYPE} \
                        --key-name ${AWS_KEYPAIR} --user-data ${userDataEncoded} --query "Instances[0].InstanceId" --output text
                        ''', returnStdout: true).trim()
                
                    // Wait until the instance is running
                    sh "aws ec2 wait instance-running --instance-ids ${instanceId}"
                    echo "Created EC2 instance: ${instanceId}"
                
                    // Get the public DNS name of the instance
                    env.INSTANCE_DNS = sh(script: "aws ec2 describe-instances --instance-ids ${instanceId} --query 'Reservations[0].Instances[0].PublicDnsName' --output text", returnStdout: true).trim()
                    // aws cloudformation create-stack --stack-name PdfToText --template-body file://ec2-cf.yaml --capabilities CAPABILITY_NAMED_IAM
                }
            }
        }
        stage('Deploy Docker on EC2') {
            when {
                branch "AWS"
            }
            steps {
                script {
                    // Install Docker on the instance and run the container
                    withCredentials([usernamePassword(credentialsId: 'Mysql-Credentials', passwordVariable: 'MYSQL_PASSWORD', usernameVariable: 'MYSQL_USER')]) {
                        sh '''
                        ssh -o StrictHostKeyChecking=no -i /var/jenkins_home/.ssh/yosi-kp.pem ec2-user@${INSTANCE_DNS} '
                            //sudo yum update -y 
                            //sudo yum install docker -y 
                            //sudo service docker start 
                            sudo docker pull '${dockerimagenamefeat}' 
                            //sudo aws s3 cp s3://firstbucket-yosi/compose.yaml /home/ec2-user/compose.yaml
                            //sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                            //sudo chmod +x /usr/local/bin/docker-compose
                            echo "MYSQL_USER='${MYSQL_USER}'" > .env 
                            echo "MYSQL_PASSWORD='${MYSQL_PASSWORD}'" >> .env 
                            sudo docker-compose up 
                        '
                        '''
                    }
                }
            }
        }

        stage('Run Docker Container') {
            when {
                expression {
                             return env.BRANCH_NAME != 'AWS';
                       }     
            }
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