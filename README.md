🚀 Flask CI/CD Pipeline with JenkinsThis project demonstrates a complete CI/CD pipeline using Jenkins Declarative syntax to build, test, and deploy a Python Flask application.📁 Project StructurePlaintextDevOps/


├── Jenkinsfile            # Pipeline definition
├── README.md              # Project documentation
└── app/
    ├── app.py             # Flask REST API
    ├── requirements.txt   # Dependencies
    ├── test_unit.py       # 7 Unit tests
    └── test_integration.py # 3 Integration tests

    
🛠 Features & EndpointsThe Flask application serves a simple REST API with the following endpoints:EndpointDescriptionGET /Home page 
Returns app statusGET /healthHealth check — Returns "healthy"GET /api/helloGreeting endpointGET /api/versionReturns current app version⛓️
Pipeline ArchitectureThe Jenkins pipeline is designed for speed, running tests in parallel to reduce total build time.Pipeline StagesCheckout:
Pulls source code from GitHub.Build: Sets up a Python virtual environment (venv) and installs requirements.Test (Parallel):Unit Tests (7):
Validates individual function logic and status codes.Integration Tests (3): Validates full API responses and JSON headers.Package:
Compresses the app into flask-app.tar.gz.Deploy: Simulates deployment and logs build metadata.Post-Build ActionsAlways: 
Archives the .tar.gz artifact for later use.Success: Reports the build URL and successful completion.Failure: 
Identifies the specific stage that caused the break.⚙️ Infrastructure & SetupJenkins ConfigurationController: 
Hosted on EC2 (Public Subnet) at 51.20.40.253:8080.Agent: Dedicated Linux runner in a Private Subnet (10.0.10.35).Job Type:
Multibranch Pipeline (auto-discovers branches and PRs).Local DevelopmentTo run the application on your local machine:Bashcd app

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
Note: Access the app locally at http://localhost:5000

<img width="1366" height="574" alt="image" src="https://github.com/user-attachments/assets/158b42cf-8ec4-46f3-9d5a-ca008ffe394c" />
