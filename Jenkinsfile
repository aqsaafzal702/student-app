pipeline {
    agent any
    
    environment {
        TEST_EMAIL = 'aqsaafzal670@gmail.com'
        TEST_PASS = '123'
        SENDER_EMAIL = 'aqsaafzal670@gmail.com'  
    }
    
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
               cd /host-ubuntu/student-app
               docker-compose -f docker-compose.yml up -d
               sleep 15
           '''
       }
   }
        
        stage('Run Selenium Tests') {
            steps {
                echo 'Running automated test cases...'
                script {
                    def testResult = sh(
                        script: '''
                           cd /host-ubuntu/assignment3-tests
                            python3 -m venv venv
                            . venv/bin/activate
                            pip3 install -r requirements.txt
                            python3 test_login.py
                            python3 test_students.py
                            python3 test_courses.py
                            python3 test_additional.py
                        ''',
                        returnStatus: true
                    )
                    env.TEST_STATUS = (testResult == 0) ? 'ALL 15 TESTS PASSED' : 'SOME TESTS FAILED'
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed!'
            emailext (
                to: 'aqsaafzal670@gmail.com',  
                subject: "Assignment 3 TEST Results: ${env.TEST_STATUS}",
                body: """
                    <h2>Test Execution Report</h2>
                    <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                    <p><strong>Build Number:</strong> #${env.BUILD_NUMBER}</p>
                    <p><strong>Test Status:</strong> ${env.TEST_STATUS}</p>
                    <p><strong>Console Output:</strong> <a href='${env.BUILD_URL}console'>View Full Logs</a></p>
                    <hr>
                    <p>15 Selenium test cases executed</p>
                    <p>Browser: Chrome (headless mode)</p>
                    <p>Test Account: aqsaafzal670@gmail.com</p>
                """,
                mimeType: 'text/html',
                from: "${SENDER_EMAIL}"
            )
        }
    }
}
