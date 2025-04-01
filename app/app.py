from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    return """
    <h1>Welcome to my containerized Python app!</h1>
    <p>Try these endpoints:</p>
    <ul>
        <li><a href="/host">/host</a> - Show container hostname</li>
        <li><a href="/env">/env</a> - Show environment variables</li>
        <li><a href="/health">/health</a> - Health check endpoint</li>
    </ul>
    """

@app.route('/host')
def host_info():
    hostname = socket.gethostname()
    return jsonify(
        message=f"Container hostname: {hostname}",
        hostname=hostname
    )

@app.route('/env')
def show_env():
    env_vars = {key: value for key, value in os.environ.items()}
    return jsonify(environment_variables=env_vars)

@app.route('/health')
def health_check():
    return jsonify(status="healthy", message="Application is running")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)