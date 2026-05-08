pipeline {
    agent any
    
    triggers {
        githubPush()  // Auto-trigger on push
    }
    
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
                    docker-compose -f docker-compose.yml down > /dev/null 2>&1 || true
                    docker-compose -f docker-compose.yml up -d
                    
                    echo "Waiting 180s for MySQL..."
                    sleep 180
                    
                    # Create database
                    docker exec student-app-db mysql -u root -proot123 -e "CREATE DATABASE IF NOT EXISTS student_db;" 2>/dev/null || true
                    
                    echo "Waiting 60s for app..."
                    sleep 60
                    
                    # Register test user via API (reliable)
                    echo "Registering test user via /auth/signup..."
                    curl -s -X POST http://13.61.194.93:3001/auth/signup \
                      -H "Content-Type: application/json" \
                      -d '{"username":"Test User","email":"aqsaafzal670@gmail.com","password":"123"}' \
                      -o /dev/null || true
                    sleep 3
                    
                    # Health check
                    echo "Checking app health..."
                    for i in 1 2 3 4 5; do
                        if curl -sf --max-time 10 http://13.61.194.93:3001/auth/login > /dev/null 2>&1; then
                            echo "App is ready"
                            break
                        fi
                        sleep 10
                    done
                '''
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running Selenium tests...'
                script {
                    def result = sh(
                        script: '''
                            cd assignment3-tests
                            python3 -m venv venv
                            . venv/bin/activate
                            pip3 install selenium==4.18.1 -q
                            python3 test_login.py && \
                            python3 test_students.py && \
                            python3 test_courses.py && \
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
                        error('Tests failed!')
                    }
                }
            }
        }
    }
    
    post {
        success {
            script {
                def author = sh(script: "git log -1 --pretty=format:'%ae'", returnStdout: true).trim()
                mail to: author,
                     subject: "Assignment 3: ALL TESTS PASSED",
                     body: "Build: ${env.BUILD_NUMBER}\nConsole: ${env.BUILD_URL}console\n\n19 Selenium tests passed!"
                echo "Email sent to ${author}"
            }
        }
        failure {
            script {
                def author = sh(script: "git log -1 --pretty=format:'%ae'", returnStdout: true).trim()
                mail to: author,
                     subject: " Assignment 3: TESTS FAILED",
                     body: "Build: ${env.BUILD_NUMBER}\nConsole: ${env.BUILD_URL}console\n\nCheck logs for details."
                echo "Failure email sent to ${author}"
            }
        }
        always {
            echo 'Pipeline completed - containers still running (manual down if needed)'
            // NO auto-down - you control manually
        }
    }
}
