pipeline {
    agent any

    environment {
        SCANNER_HOME = tool 'sonar-scanner'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Tools') {
            steps {
                sh '''
                python3 --version
                docker --version
                docker compose version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m pip install --break-system-packages -r requirements.txt
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh "${SCANNER_HOME}/bin/sonar-scanner"
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                docker build -t employeefeedback-flask:latest .
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker compose down
                docker compose up -d
                '''
            }
        }
    }
}

