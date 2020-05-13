from flask import Flask, jsonify, request
from flask_cors import CORS
from settings import TOKEN
import random
import os
import re


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


def random_str():
    base = [i for i in range(48, 58)]
    base.extend([i for i in range(65, 91)])
    base.extend([i for i in range(97, 123)])
    ans = []
    for i in range(5):
        ans.append(random.choice(base))
    return ''.join([chr(i) for i in ans])


@app.route('/add', methods=['GET'])
def easy_download():
    token = request.json.get('token')
    if token != TOKEN:
        return jsonify({"error": 1, "msg": "TOKEN error"})
    user = request.json.get('user')
    pwd = request.json.get('pwd')
    if re.findall('[a-z][A-Z][0-9][_-]', user) != user:
        return jsonify({"error": 1, "msg": "大神 别搞我"})
    if re.findall('[a-z][A-Z][0-9][_-]', pwd) != pwd:
        return jsonify({"error": 1, "msg": "大神 别搞我"})
    urls = request.json.get('urls', '')
    task_id = random_str()
    task_path = '/home/data/{}'.format(task_id)
    os.mkdir(task_path)
    with open('{}/urls.txt'.format(task_path), 'wr') as f:
        f.write(urls)
    os.system('wget -f {0}/urls.txt -P {0} --user={1} --password={2} > {0}/download.out 2>&1 &'.format(task_path, user, pwd))
    return jsonify({"error": 0, "msg": "/easyDownload/info?taskId={}".format(task_id)})


@app.route('/get', methods=['GET'])
def easy_download():
    token = request.json.get('token')
    if token != TOKEN:
        return jsonify({"error": 1, "msg": "TOKEN error"})
    user = request.json.get('user')
    pwd = request.json.get('pwd')
    urls = request.json.get('urls', '')
    task_id = random_str()
    task_path = '/home/data/{}'.format(task_id)
    os.mkdir(task_path)
    with open('{}/urls.txt'.format(task_path), 'wr') as f:
        f.write(urls)
    os.system('wget -f {0}/urls.txt -P {0} --user={1} --password={2} > {0}/download.out 2>&1 &'.format(task_path, user, pwd))
    return jsonify({"error": 0, "msg": "/easyDownload/info?taskId={}".format(task_id)})


if __name__ == '__main__':
    app.run()
