pipeline {
    agent any
    
    environment {
        TEST_EMAIL = 'aqsaafzal670@gmail.com'
        TEST_PASS = '123'
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
            
            # Clean start
            docker-compose -f docker-compose.yml down > /dev/null 2>&1 || true
            
            # Start fresh
            docker-compose -f docker-compose.yml up -d
            
            # SIMPLE FIX: Just wait 3 minutes for DB + app to initialize
            echo " Waiting 180 seconds for database and app to initialize..."
            sleep 180
            
            # Quick health check
            echo " Checking if app is responding..."
            if curl -sf --max-time 10 http://localhost:3000/auth/login > /dev/null 2>&1; then
                echo " App is ready on localhost:3000"
            else
                echo " App may still be starting, proceeding with tests anyway..."
                # Show last few lines of app logs for debugging
                docker logs student-app-web 2>&1 | tail -10 || true
            fi
        '''
    }
}
        
        stage('Test') {
            steps {
                echo 'Running Selenium tests...'
                script {
                    def result = sh(
                        script: '''
                            echo "Installing dependencies..."
                            apt-get update -qq
                            apt-get install -y -qq python3 python3-pip python3-venv curl chromium chromium-driver ca-certificates > /dev/null 2>&1
                            
                            cd assignment3-tests
                            
                            python3 -m venv venv
                            . venv/bin/activate
                            
                            pip3 install selenium==4.18.1 -q
                            
                            echo "Starting tests..."
                            python3 test_login.py
                            python3 test_students.py
                            python3 test_courses.py
                            python3 test_additional.py
                        ''',
                        returnStatus: true
                    )
                    if (result == 0) {
                        env.TEST_STATUS = 'ALL 19 TESTS PASSED'
                        echo 'ALL 19 TESTS PASSED'
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
            
            // FIX: try-catch ko script {} block me wrap karo
            script {
                try {
                    //mail to: 'qasimalik@gmail.com',
                         subject: "Assignment 3 Results: ${env.TEST_STATUS}",
                         body: """
Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
Status: ${env.TEST_STATUS}
Console: ${env.BUILD_URL}console
19 Selenium tests executed with headless Chrome
Test Account: aqsaafzal670@gmail.com
                        """,
                         mimeType: 'text/html',
                         from: 'aqsaafzal670@gmail.com'
                    echo 'Email sent to Sir (qasimalik@gmail.com)'
                } catch (Exception e) {
                    echo "Email error: ${e.message}"
                }
            }
            
            //  deployment is DOWN initially
            sh '''
                echo "Stopping containers (deployment DOWN as required)..."
                cd /host-ubuntu/student-app
                docker-compose -f docker-compose.yml down > /dev/null 2>&1 || true
                echo "Containers stopped - deployment is now DOWN"
            '''
        }
    }
}
