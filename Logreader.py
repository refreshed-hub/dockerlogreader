from flask import Flask, jsonify, render_template
import docker

app = Flask(__name__)
client = docker.from_env()


def list_containers():
    containers = client.containers.list()
    return [container.name for container in containers]


@app.route('/containers', methods=['GET'])
def fetch_containers():
    return jsonify({'containers': list_containers()})


@app.route('/logs/<container_name>', methods=['GET'])
def fetch_logs(container_name):
    try:
        container = client.containers.get(container_name)
        logs = container.logs().decode('utf-8')
        return f"<pre>{logs}</pre>"
    except docker.errors.NotFound:
        return 'Container not found', 404


@app.route('/')
def index():
    containers = list_containers()
    return render_template('index.html', containers=containers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
