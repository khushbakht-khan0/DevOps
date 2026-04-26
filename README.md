# DevOps Assignment 4 - CI/CD Pipeline

## Project Structure
```
DevOps/
├── Jenkinsfile          # Main pipeline
├── app/
│   ├── app.py           # Flask application
│   ├── test_unit.py     # Unit tests (7 tests)
│   ├── test_integration.py  # Integration tests (3 tests)
│   └── requirements.txt # Python dependencies
└── README.md
```

## How to Run Locally
```bash
cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## API Endpoints
- `GET /` - Home
- `GET /health` - Health check
- `GET /api/hello` - Hello endpoint
- `GET /api/version` - Version info

## Pipeline Stages
1. Checkout
2. Build
3. Test (Parallel: Unit + Integration)
4. Package
5. Deploy
