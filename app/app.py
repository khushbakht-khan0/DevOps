from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "DevOps Assignment 4 - Flask App",
        "status": "running"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "flask-app"
    }), 200

@app.route('/api/hello')
def hello():
    return jsonify({
        "message": "Hello from Flask!"
    }), 200

@app.route('/api/version')
def version():
    return jsonify({
        "version": "1.0.0",
        "app": "devops-flask-app"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
