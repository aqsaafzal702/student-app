pipeline {
    agent any
    
    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning repository from GitHub...'
                git branch: 'main', 
                    url: 'https://github.com/aqsaafzal702/student-app.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    docker.build("aqsaafzal99/student-app-jenkins:v1")
                }
            }
        }
        
        stage('Deploy with Docker Compose') {
            steps {
                echo 'Deploying containers...'
                sh '''
                    cd /var/jenkins_home/workspace/student-app-pipeline
                    docker compose -f docker-compose-jenkins.yml up -d
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed!'
        }
    }
}
