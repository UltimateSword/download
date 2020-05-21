from flask import Flask, jsonify, request
from flask_cors import CORS
from settings import TOKEN
from models import Download, db
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
    for i in range(8):
        ans.append(random.choice(base))
    return ''.join([chr(i) for i in ans])


@app.route('/add', methods=['POST'])
def add_download():
    token = request.json.get('token')
    if token != TOKEN:
        return jsonify({"error": 1, "msg": "TOKEN error"})
    user = request.json.get('user', '')
    pwd = request.json.get('pwd', '')
    if re.findall('[a-z][A-Z][0-9][_-]', user) != user:
        return jsonify({"error": 1, "msg": "大佬 别注入了"})
    if re.findall('[a-z][A-Z][0-9][_-]', pwd) != pwd:
        return jsonify({"error": 1, "msg": "大佬 别注入了"})
    urls = request.json.get('urls', '')
    task_id = random_str()
    task_path = '/home/data/{}'.format(task_id)
    os.mkdir(task_path)
    urls = [i for i in urls.split('\n') if i]
    if len(urls) > 10000:
        return jsonify({"error": 1, "msg": "待下载url不能超过10000"})
    to_be_insert = []
    for i, j in enumerate(urls):
        to_be_insert.append(Download(user=user, pwd=pwd, url=j, task_id=task_id))
    db.session.add_all(to_be_insert)
    db.commit()
    return jsonify({"error": 0, "msg": "/get?taskId={}".format(task_id)})


@app.route('/get', methods=['GET'])
def get_download():
    task_id = request.args.get("task_id")
    tasks = Download.query.filter_by(task_id=task_id)



if __name__ == '__main__':
    app.run()
