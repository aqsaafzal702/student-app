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
                    docker exec student-app-db mysql -u root -proot123 -e "CREATE DATABASE IF NOT EXISTS student_db;" 2>/dev/null || true
                    docker exec student-app-db mysql -u root -proot123 -e "GRANT ALL PRIVILEGES ON student_db.* TO 'root'@'%'; FLUSH PRIVILEGES;" 2>/dev/null || true
                    echo "Waiting 60s for app..."
                    sleep 60
                    echo "Checking app health on port 3001..."
                    for i in 1 2 3 4 5; do
                        if curl -sf --max-time 10 http://13.61.194.93:3001/auth/login > /dev/null 2>&1; then
                            echo "App is ready on port 3001"
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
                            apt-get update -qq
                            apt-get install -y -qq python3 python3-pip python3-venv curl chromium chromium-driver ca-certificates > /dev/null 2>&1
                            cd assignment3-tests
                            python3 -m venv venv
                            . venv/bin/activate
                            pip3 install selenium==4.18.1 webdriver-manager==4.0.1 -q
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
            script {
                def status = env.TEST_STATUS ?: 'UNKNOWN'
                def subjectLine = 'Assignment 3 Results: ' + status
                def bodyText = 'Status: ' + status + '\nConsole: ' + env.BUILD_URL + 'console'
                mail to: 'aqsaafzal670@gmail.com', subject: subjectLine, body: bodyText
                echo 'Email sent to Sir'
            }
            sh '''
                echo "Stopping containers (deployment DOWN as required)..."
                cd /host-ubuntu/student-app
                docker-compose -f docker-compose.yml down > /dev/null 2>&1 || true
                echo "Containers stopped - deployment is now DOWN"
            '''
        }
    }
}
