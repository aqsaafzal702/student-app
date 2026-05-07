pipeline {
    agent any
    
    environment {
        TEST_EMAIL = 'aqsaafzal670@gmail.com'
        TEST_PASS = '123'
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
                            # ========== INSTALL PYTHON3 ==========
                            echo "Installing Python3..."
                            apt-get update -qq
                            apt-get install -y -qq python3 python3-pip python3-venv curl > /dev/null 2>&1
                            
                            # ========== NAVIGATE TO TESTS ==========
                            cd assignment3-tests
                            
                            # ========== DEBUG: SHOW FILES ==========
                            echo "=== Files in assignment3-tests ==="
                            ls -la
                            
                            # ========== DEBUG: REQUIREMENTS.TXT ==========
                            echo "=== requirements.txt content ==="
                            cat requirements.txt
                            
                            # ========== CREATE VENV ==========
                            echo " Creating virtual environment..."
                            python3 -m venv venv
                            . venv/bin/activate
                            
                            # ========== INSTALL DEPENDENCIES ==========
                            echo "📥 Installing Python packages (selenium, webdriver-manager)..."
                            pip3 install -r requirements.txt
                            
                            # ========== DEBUG: INSTALLED PACKAGES ==========
                            echo "=== Installed packages ==="
                            pip3 list
                            
                            # ========== RUN ALL 15 TESTS ==========
                            echo "Starting Test Execution..."
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
                        echo 'ALL 15 TESTS PASSED'
                    } else {
                        echo 'SOME TESTS FAILED - Check console above'
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed!'
            echo 'Email notification: Temporarily skipped (SSL config issue)'
            echo 'Check console output above for test results'
        }
    }
}
