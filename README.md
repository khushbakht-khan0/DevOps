# Assignment 4 - Task 2: Declarative Pipeline with Parallel Stages

## Overview
This task implements a complete CI/CD pipeline using Jenkins Declarative Pipeline syntax. The pipeline builds, tests, packages, and deploys a Python Flask application. Unit and integration tests run in parallel to reduce build time.

---

## Project Structure
```
DevOps/
├── Jenkinsfile              # Main declarative pipeline
├── README.md                # Project documentation
└── app/
    ├── app.py               # Flask application
    ├── requirements.txt     # Python dependencies
    ├── test_unit.py         # 7 unit tests
    └── test_integration.py  # 3 integration tests
```

---

## Flask Application

Sample application built using Python Flask with the following REST API endpoints:

| Endpoint | Description |
|---|---|
| `GET /` | Home page — returns app status |
| `GET /health` | Health check — returns healthy status |
| `GET /api/hello` | Hello endpoint — returns greeting |
| `GET /api/version` | Version info — returns app version |

---

## Test Suite

### Unit Tests (7 tests)
- `test_home_status_code` — Verifies home returns HTTP 200
- `test_home_returns_json` — Verifies home returns JSON with status field
- `test_health_status_code` — Verifies health returns HTTP 200
- `test_health_returns_healthy` — Verifies health status is 'healthy'
- `test_hello_endpoint` — Verifies hello returns HTTP 200
- `test_hello_returns_message` — Verifies hello contains message field
- `test_version_endpoint` — Verifies version returns HTTP 200

### Integration Tests (3 tests)
- `test_health_check_full_response` — Verifies complete health response structure
- `test_version_full_response` — Verifies complete version response with all fields
- `test_content_type_is_json` — Verifies Content-Type header is application/json

---

## Pipeline Stages

| Stage | Description |
|---|---|
| Checkout | Clones code from GitHub repository |
| Build | Creates Python venv and installs dependencies |
| Test (Parallel) | Runs Unit Tests and Integration Tests concurrently |
| Package | Creates flask-app.tar.gz archive |
| Deploy | Deployment step with build info |

---

## Parallel Test Execution

The Test stage uses Jenkins `parallel` block to run unit and integration tests simultaneously. Each branch publishes its own JUnit XML report. If either branch fails, the entire pipeline fails.

```groovy
stage('Test') {
    parallel {
        stage('Unit Tests') { ... }
        stage('Integration Tests') { ... }
    }
}
```

---

## Post Actions

| Handler | Action |
|---|---|
| `always` | Archives flask-app.tar.gz as build artifact |
| `success` | Prints success message with build URL |
| `failure` | Prints failure message with failing stage info |

---

## Multibranch Pipeline Setup

- Job Name: `devops-flask-app`
- Branch Source: GitHub — `khushbakht-khan0/DevOps`
- Jenkinsfile auto-detected in repository root
- Build triggered automatically on every push

---

## Build Results

| Build | Result | Reason |
|---|---|---|
| #1 | FAILED | python3-venv not installed on agent |
| #2 | SUCCESS | All 10 tests passed, artifact archived |

---

## Jenkins Configuration

- Jenkins Controller: EC2 Public Subnet — `51.20.40.253:8080`
- Jenkins Agent: EC2 Private Subnet — `10.0.10.35` (label: `linux-agent`)
- Pipeline runs on `linux-agent` (not built-in node)
- GitHub credentials configured via Personal Access Token

---

## How to Run Locally

```bash
cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Then open browser at: `http://localhost:5000`
