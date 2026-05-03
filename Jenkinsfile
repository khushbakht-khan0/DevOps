@Library('jenkins-shared-library') _

pipeline {
    agent { label 'linux-agent' }

    environment {
        APP_DIR = 'app'
        VENV_DIR = 'venv'
        SONAR_TOKEN = 'squ_9d6a2dd07f91849e55f4bd5bf950196565d4d48c'
        AWS_REGION = 'eu-north-1'
        ECR_REPO = '587721667106.dkr.ecr.eu-north-1.amazonaws.com/devops-flask-app'
        IMAGE_TAG = "${env.GIT_COMMIT?.take(7) ?: 'latest'}"
        BRANCH_TAG = "${env.GIT_BRANCH?.replaceAll('/', '-') ?: 'main'}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Installing dependencies...'
                sh '''
                    cd ${APP_DIR}
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Static Analysis') {
            steps {
                echo 'Running SonarQube Analysis...'
                withSonarQubeEnv('SonarQube') {
                    sh "sonar-scanner -Dsonar.projectKey=DevOps-Flask-App -Dsonar.projectName='DevOps Flask App' -Dsonar.sources=app -Dsonar.language=py -Dsonar.python.version=3 -Dsonar.host.url=http://10.0.1.87:9000 -Dsonar.login=${SONAR_TOKEN}"
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo 'Quality Gate check skipped - webhook not configured'
            }
        }

        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        echo 'Running Unit Tests...'
                        sh '''
                            cd ${APP_DIR}
                            . ${VENV_DIR}/bin/activate
                            python3 -m pytest test_unit.py -v --junit-xml=unit-test-results.xml
                        '''
                    }
                    post {
                        always {
                            junit 'app/unit-test-results.xml'
                        }
                    }
                }
                stage('Integration Tests') {
                    steps {
                        echo 'Running Integration Tests...'
                        sh '''
                            cd ${APP_DIR}
                            . ${VENV_DIR}/bin/activate
                            python3 -m pytest test_integration.py -v --junit-xml=integration-test-results.xml
                        '''
                    }
                    post {
                        always {
                            junit 'app/integration-test-results.xml'
                        }
                    }
                }
            }
        }

        stage('Container Build') {
            steps {
                echo 'Building Docker image...'
                sh """
                    docker build -t ${ECR_REPO}:${IMAGE_TAG} -t ${ECR_REPO}:${BRANCH_TAG} .
                    echo "Image built successfully!"
                """
            }
        }

        stage('Security Scan') {
            steps {
                echo 'Running Trivy vulnerability scan...'
                sh """
                    trivy image \
                        --exit-code 0 \
                        --severity HIGH,CRITICAL \
                        --ignore-unfixed \
                        --ignorefile .trivyignore \
                        --format table \
                        --output trivy-report.txt \
                        ${ECR_REPO}:${IMAGE_TAG}
                    cat trivy-report.txt
                """
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-report.txt', allowEmptyArchive: true
                }
            }
        }

        stage('Push to ECR') {
            steps {
                echo 'Pushing to ECR...'
                sh """
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin 587721667106.dkr.ecr.eu-north-1.amazonaws.com
                    docker push ${ECR_REPO}:${IMAGE_TAG}
                    docker push ${ECR_REPO}:${BRANCH_TAG}
                    echo "Images pushed successfully!"
                """
            }
        }

        stage('Package') {
            steps {
                echo 'Packaging application...'
                sh '''
                    tar --exclude=app/venv --exclude=app/__pycache__ -czf flask-app.tar.gz app/
                    ls -lh flask-app.tar.gz
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying...'
                sh '''
                    echo "Build: ${BUILD_NUMBER}"
                    echo "Branch: ${GIT_BRANCH}"
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'flask-app.tar.gz', allowEmptyArchive: true
        }
        success {
            notifySlack(message: "Build PASSED: ${env.JOB_NAME} #${env.BUILD_NUMBER} | Branch: ${env.GIT_BRANCH} | ${env.BUILD_URL}", color: 'good')
        }
        failure {
            notifySlack(message: "Build FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER} | Branch: ${env.GIT_BRANCH} | ${env.BUILD_URL}", color: 'danger')
        }
    }
}
