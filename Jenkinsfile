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
                echo ' Cloning repository from GitHub...'
                git branch: 'main', 
                    url: 'https://github.com/aqsaafzal702/student-app.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo ' Building Docker image...'
                script {
                    docker.build("aqsaafzal99/student-app-jenkins:v1")
                }
            }
        }
        
        stage('Deploy with Docker Compose') {
            steps {
                echo ' Deploying containers...'
                sh '''
                    cd /host-ubuntu/student-app
                    docker-compose -f docker-compose.yml up -d
                    sleep 15
                '''
            }
        }
        
        stage('Run Selenium Tests') {
            steps {
                echo ' Running automated test cases...'
                script {
                    def testResult = sh(
                        script: '''
                            # ========== INSTALL PYTHON3 + CHROMIUM ==========
                            echo " Installing Python3 + Chromium..."
                            apt-get update -qq
                            apt-get install -y -qq python3 python3-pip python3-venv curl chromium chromium-driver > /dev/null 2>&1
                            
                            # Set Chrome path for Selenium
                            export CHROME_BIN=/usr/bin/chromium
                            
                            # ========== NAVIGATE TO TESTS ==========
                            cd assignment3-tests
                            
                            # ========== CREATE VENV ==========
                            echo " Creating virtual environment..."
                            python3 -m venv venv
                            . venv/bin/activate
                            
                            # ========== INSTALL DEPENDENCIES ==========
                            echo " Installing selenium + webdriver-manager..."
                            pip3 install -r requirements.txt -q
                            
                            # ========== RUN ALL 15 TESTS ==========
                            echo " Starting Test Execution..."
                            echo "================================"
                            python3 test_login.py
                            python3 test_students.py
                            python3 test_courses.py
                            python3 test_additional.py
                            echo "================================"
                        ''',
                        returnStatus: true
                    )
                    if (testResult == 0) {
                        env.TEST_STATUS = ' ALL 15 TESTS PASSED'
                        echo ' ALL 15 TESTS PASSED'
                    } else {
                        env.TEST_STATUS = ' SOME TESTS FAILED'
                        echo ' SOME TESTS FAILED'
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo ' Pipeline completed!'
            
            // ========== EMAIL NOTIFICATION ==========
            // Note: May fail due to SSL config in Jenkins container
            // But keeping it here as per assignment requirement
            script {
                try {
                    mail to: 'aqsaafzal670@gmail.com',
                         subject: " Assignment 3 Results: ${env.TEST_STATUS}",
                         body: """
Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
Status: ${env.TEST_STATUS}
Console: ${env.BUILD_URL}console

15 Selenium tests executed (headless Chrome)
Test Account: aqsaafzal670@gmail.com
Test Code: assignment3-tests/ folder
                        """
                    echo ' Email sent successfully'
                } catch (Exception e) {
                    echo ' Email failed (SSL config issue) - Check console for test results'
                }
            }
            
            echo ' Check console output above for detailed test results'
        }
    }
}
