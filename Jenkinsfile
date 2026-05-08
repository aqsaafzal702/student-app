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
                    
                    # Create users table and insert test user
                    echo "Creating users table and test user..."
                    docker exec student-app-db mysql -u root -proot123 student_db << 'EOSQL'
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email, password, role) 
VALUES (
    'Test User', 
    'aqsaafzal670@gmail.com', 
    '$2b$10$CwTycUXWue0Thq9StjUM0uHk8fX.gPJbz.jANFLqjVqLNPjqVz1GK',
    'user'
)
ON DUPLICATE KEY UPDATE email=email;
EOSQL
                    
                    echo "Test user created!"
                    
                    # Health check
                    echo "Checking app health on port 3001..."
                    for i in 1 2 3 4 5; do
                        if curl -sf --max-time 10 http://13.61.194.93:3001/auth/login > /dev/null 2>&1; then
                            echo "App is ready"
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
                        error('Tests failed!')
                    }
                }
            }
        }
    }
    
    post {
        success {
            script {
                // Get commit author email dynamically
                def commitAuthor = sh(
                    script: "git log -1 --pretty=format:'%ae'",
                    returnStdout: true
                ).trim()
                
                def buildNum = env.BUILD_NUMBER
                def jobName = env.JOB_NAME
                def buildUrl = env.BUILD_URL
                
                def emailBody = """
Job: ${jobName}
Build: #${buildNum}
Status: ALL 19 TESTS PASSED
Console: ${buildUrl}console

19 Selenium tests executed successfully!
Test Account: aqsaafzal670@gmail.com / 123
                """
                
                // Send email to commit author
                mail to: commitAuthor,
                     subject: "Assignment 3: ALL 19 TESTS PASSED (Build #${buildNum})",
                     body: emailBody,
                     mimeType: 'text/html'
                
                echo "Email sent to ${commitAuthor}"
            }
        }
        
        failure {
            script {
                // Get commit author email dynamically
                def commitAuthor = sh(
                    script: "git log -1 --pretty=format:'%ae'",
                    returnStdout: true
                ).trim()
                
                def buildNum = env.BUILD_NUMBER
                def jobName = env.JOB_NAME
                def buildUrl = env.BUILD_URL
                
                def emailBody = """
Job: ${jobName}
Build: #${buildNum}
Status: TESTS FAILED
Console: ${buildUrl}console

Please check the console output for details.
                """
                
                // Send failure email to commit author
                mail to: commitAuthor,
                     subject: "Assignment 3: TESTS FAILED (Build #${buildNum})",
                     body: emailBody,
                     mimeType: 'text/html'
                
                echo "Failure email sent to ${commitAuthor}"
            }
        }
    }
}
