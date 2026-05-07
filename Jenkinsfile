pipeline {
    agent any
    
    environment {
        TEST_EMAIL = 'aqsaafzal670@gmail.com'
        TEST_PASS = '123'
        SENDER_EMAIL = 'aqsaafzal670@gmail.com'
    }
    
    stages {
        stage('Clone') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/aqsaafzal702/student-app.git'
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                script {
                    docker.build("aqsaafzal99/student-app-jenkins:v1")
                }
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying containers...'
                sh '''
                    cd /host-ubuntu/student-app
                    docker-compose -f docker-compose.yml up -d
                    sleep 15
                '''
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running Selenium tests...'
                script {
                    def result = sh(
                        script: '''
                            # Install Python + Chromium (system packages)
                            echo "Installing dependencies..."
                            apt-get update -qq
                            apt-get install -y -qq python3 python3-pip python3-venv curl chromium chromium-driver > /dev/null 2>&1
                            
                            cd assignment3-tests
                            
                            # Create virtual environment
                            python3 -m venv venv
                            . venv/bin/activate
                            
                            # Install only selenium (no webdriver-manager)
                            pip3 install selenium==4.18.1 -q
                            
                            # Run all 15 tests
                            echo "Starting tests..."
                            python3 test_login.py
                            python3 test_students.py
                            python3 test_courses.py
                            python3 test_additional.py
                        ''',
                        returnStatus: true
                    )
                    if (result == 0) {
                        env.TEST_STATUS = 'ALL 15 TESTS PASSED'
                        echo 'ALL 15 TESTS PASSED'
                    } else {
                        env.TEST_STATUS = 'SOME TESTS FAILED'
                        echo 'SOME TESTS FAILED'
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed!'
            script {
                try {
                    mail to: 'aqsaafzal670@gmail.com',
                         subject: "Assignment 3: ${env.TEST_STATUS}",
                         body: """
Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
Status: ${env.TEST_STATUS}
Console: ${env.BUILD_URL}console
15 Selenium tests executed
                        """
                    echo 'Email sent'
                } catch (e) {
                    echo 'Email failed (SSL) - Check console'
                }
            }
        }
    }
}
