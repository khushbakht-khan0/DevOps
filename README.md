1. Overview
This task implements a complete CI/CD pipeline using Jenkins Declarative Pipeline syntax. The pipeline builds, tests, packages, and deploys a Python Flask application. Unit and integration tests run in parallel to reduce build time.

2. Project Structure
DevOps/
├── Jenkinsfile              # Main declarative pipeline
├── README.md               # Project documentation
└── app/
    ├── app.py              # Flask application
    ├── requirements.txt    # Python dependencies
    ├── test_unit.py        # 7 unit tests
    └── test_integration.py # 3 integration tests

3. Flask Application
The sample application is built using Python Flask framework and exposes the following REST API endpoints:

Endpoint	Description
GET /	Home page — returns app status
GET /health	Health check — returns healthy status
GET /api/hello	Hello endpoint — returns greeting
GET /api/version	Version info — returns app version

4. Test Suite
4.1 Unit Tests (7 tests)
•test_home_status_code — Verifies home returns HTTP 200
•test_home_returns_json — Verifies home returns JSON with status field
•test_health_status_code — Verifies health returns HTTP 200
•test_health_returns_healthy — Verifies health status is 'healthy'
•test_hello_endpoint — Verifies hello returns HTTP 200
•test_hello_returns_message — Verifies hello contains message field
•test_version_endpoint — Verifies version returns HTTP 200

4.2 Integration Tests (3 tests)
•test_health_check_full_response — Verifies complete health response structure
•test_version_full_response — Verifies complete version response with all fields
•test_content_type_is_json — Verifies Content-Type header is application/json

5. Pipeline Stages
Stage	Description
Checkout	Clones code from GitHub repository
Build	Creates Python venv and installs dependencies
Test (Parallel)	Runs Unit Tests and Integration Tests concurrently
Package	Creates flask-app.tar.gz archive
Deploy	Deployment step with build info

6. Parallel Test Execution
The Test stage uses Jenkins parallel block to run unit and integration tests simultaneously. Each branch publishes its own JUnit XML report. If either branch fails, the entire pipeline fails.

stage('Test') {
  parallel {
    stage('Unit Tests') { ... }
    stage('Integration Tests') { ... }
  }
}

7. Post Actions
Handler	Action
always	Archives flask-app.tar.gz as build artifact
success	Prints success message with build URL
failure	Prints failure message with failing stage info

8. Multibranch Pipeline Setup
The pipeline is configured as a Multibranch Pipeline in Jenkins to automatically discover branches and pull requests from the GitHub repository.
•Job Name: devops-flask-app
•Branch Source: GitHub — khushbakht-khan0/DevOps
•Jenkinsfile auto-detected in repository root
•Build triggered automatically on every push

9. Build Results
Build	Result
#1	FAILED — python3-venv not installed on agent
#2	SUCCESS — All 10 tests passed, artifact archived

10. Jenkins Configuration
•Jenkins Controller: EC2 Public Subnet — 51.20.40.253:8080
•Jenkins Agent: EC2 Private Subnet — 10.0.10.35 (label: linux-agent)
•Pipeline runs on linux-agent (not built-in node)
•GitHub credentials configured via Personal Access Token

11. How to Run Locally
cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py

Then open browser at: http://localhost:5000