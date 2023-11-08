from flask import Flask, jsonify, render_template, Response
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
    logs = get_logs(container_name)
    return f"<pre>{logs}</pre>"


def get_logs(container_name):
    try:
        container = client.containers.get(container_name)
        logs = container.logs().decode('utf-8')
        return f"{logs}"
    except docker.errors.NotFound:
        return 'Container not found'


@app.route('/download_logs/<container_name>')
def download_logs(container_name):
    # Assuming 'get_logs' is a function that fetches logs from a given container.
    logs = get_logs(container_name)

    # Generate a Response object with logs as the content and appropriate headers.
    return Response(
        logs,
        mimetype='text/plain',
        headers={"Content-Disposition": f"attachment;filename={container_name}_logs.txt"}
    )


@app.route('/')
def index():
    containers = list_containers()
    return render_template('index.html', containers=containers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
