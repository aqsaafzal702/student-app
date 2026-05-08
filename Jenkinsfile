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
                    docker-compose -f docker-compose.yml down > /dev/null 2>&1 || true
                    docker-compose -f docker-compose.yml up -d
                    
                    echo "Waiting 180s for MySQL..."
                    sleep 180
                    
                    # Create database
                    docker exec student-app-db mysql -u root -proot123 -e "CREATE DATABASE IF NOT EXISTS student_db;" 2>/dev/null || true
                    
                    echo "Waiting 60s for app to initialize..."
                    sleep 60
                    
                    # ✅ REGISTER TEST USER VIA API (More reliable than SQL)
                    echo "Registering test user via /auth/signup API..."
                    curl -s -X POST http://13.61.194.93:3001/auth/signup \
                      -H "Content-Type: application/json" \
                      -d '{"username":"Test User","email":"aqsaafzal670@gmail.com","password":"123"}' \
                      -w "\\nHTTP_CODE: %{http_code}\\n" -o /tmp/signup.txt 2>/dev/null || true
                    
                    echo "Signup response:"
                    cat /tmp/signup.txt 2>/dev/null || echo "(no output)"
                    
                    # Wait for DB commit
                    sleep 5
                    
                    # Verify user exists (optional debug)
                    echo "Verifying user in DB..."
                    USER_CHECK=$(docker exec student-app-db mysql -u root -proot123 student_db -N -e "SELECT COUNT(*) FROM users WHERE email='aqsaafzal670@gmail.com';" 2>/dev/null || echo "0")
                    if [ "$USER_CHECK" -ge 1 ]; then
                        echo "✅ Test user verified in database!"
                    else
                        echo "⚠️ User check: $USER_CHECK (API signup might still have succeeded)"
                    fi
                    
                    # Health check
                    echo "Checking app health on port 3001..."
                    for i in 1 2 3 4 5; do
                        if curl -sf --max-time 10 http://13.61.194.93:3001/auth/login > /dev/null 2>&1; then
                            echo "✅ App is ready"
                            break
                        fi
                        echo "Attempt $i/5: Waiting..."
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
                            echo "Installing dependencies..."
                            apt-get update -qq > /dev/null 2>&1
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
                        echo '✅ ALL 19 TESTS PASSED'
                    } else {
                        env.TEST_STATUS = 'SOME TESTS FAILED'
                        echo '❌ SOME TESTS FAILED'
                        error('Tests failed!')
                    }
                }
            }
        }
    }
    
    post {
        success {
            script {
                def commitAuthor = sh(
                    script: "git log -1 --pretty=format:'%ae'",
                    returnStdout: true
                ).trim()
                
                def emailBody = """
Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
Status: ✅ ALL 19 TESTS PASSED
Console: ${env.BUILD_URL}console

19 Selenium tests executed successfully!
Test Account: aqsaafzal670@gmail.com / 123
                """
                
                mail to: commitAuthor,
                     subject: "✅ Assignment 3: ALL 19 TESTS PASSED (Build #${env.BUILD_NUMBER})",
                     body: emailBody,
                     mimeType: 'text/html'
                
                echo "✅ Success email sent to ${commitAuthor}"
            }
        }
        
        failure {
            script {
                def commitAuthor = sh(
                    script: "git log -1 --pretty=format:'%ae'",
                    returnStdout: true
                ).trim()
                
                def emailBody = """
Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
Status: ❌ TESTS FAILED
Console: ${env.BUILD_URL}console

Please check the console output for details.
                """
                
                mail to: commitAuthor,
                     subject: "❌ Assignment 3: TESTS FAILED (Build #${env.BUILD_NUMBER})",
                     body: emailBody,
                     mimeType: 'text/html'
                
                echo "❌ Failure email sent to ${commitAuthor}"
            }
        }
    }
}
