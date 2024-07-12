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
                    // Define your Dockerfile content
                    def dockerfile = '''
                    FROM python:3.9-slim

                    WORKDIR /app

                    COPY . .

                    # Install dependencies if you have a requirements.txt
                    RUN pip install --no-cache-dir -r requirements.txt

                    CMD ["python", "app.py"]  # Replace with your entry point
                    '''

                    // Write Dockerfile to the workspace
                    writeFile file: 'Dockerfile', text: dockerfile

                    // Build the Docker image
                    sh 'docker build -t PythonAPP:latest .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                // Run the Docker container (adjust options as needed)
                sh 'docker run --rm PythonAPP:latest'
            }
        }
    }
    
    post {
        always {
            // Clean up, remove any images or containers if necessary
            sh 'docker rmi PythoAPP:latest || true'
        }
    }
}

