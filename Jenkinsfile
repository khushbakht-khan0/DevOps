pipeline {
    agent { label 'linux-agent' }

    environment {
        APP_DIR = 'app'
        VENV_DIR = 'venv'
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

        stage('Test') {
            parallel {

                stage('Unit Tests') {
                    steps {
                        echo 'Running Unit Tests...'
                        sh '''
                            cd ${APP_DIR}
                            . ${VENV_DIR}/bin/activate
                            python3 -m pytest test_unit.py -v \
                                --junit-xml=unit-test-results.xml
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
                            python3 -m pytest test_integration.py -v \
                                --junit-xml=integration-test-results.xml
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

        stage('Package') {
            steps {
                echo 'Packaging application...'
                sh '''
                    tar --exclude=app/venv \
                        --exclude=app/__pycache__ \
                        -czf flask-app.tar.gz app/
                    echo "Package created: flask-app.tar.gz"
                    ls -lh flask-app.tar.gz
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sh '''
                    echo "Deployment step - App packaged successfully"
                    echo "Build: ${BUILD_NUMBER}"
                    echo "Branch: ${GIT_BRANCH}"
                '''
            }
        }

    }

    post {
        always {
            echo 'Archiving build artifacts...'
            archiveArtifacts artifacts: 'flask-app.tar.gz', 
                             allowEmptyArchive: true
        }
        success {
            echo "Build #${BUILD_NUMBER} SUCCESSFUL on branch ${GIT_BRANCH}"
            mail to: 'khushbakhtkhan868@gmail.com',
                 subject: "Jenkins Build SUCCESS: ${JOB_NAME} #${BUILD_NUMBER}",
                 body: """
                 Build Successful!
                 Job: ${JOB_NAME}
                 Build Number: ${BUILD_NUMBER}
                 Branch: ${GIT_BRANCH}
                 URL: ${BUILD_URL}
                 """
        }
        failure {
            echo "Build #${BUILD_NUMBER} FAILED on branch ${GIT_BRANCH}"
            mail to: 'khushbakhtkhan868@gmail.com',
                 subject: "Jenkins Build FAILED: ${JOB_NAME} #${BUILD_NUMBER}",
                 body: """
                 Build Failed!
                 Job: ${JOB_NAME}
                 Build Number: ${BUILD_NUMBER}
                 Branch: ${GIT_BRANCH}
                 URL: ${BUILD_URL}
                 """
        }
    }
}
