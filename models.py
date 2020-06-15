from datetime import datetime
from ext import db


"""
CREATE TABLE DOWNLOAD(
   ID integer PRIMARY KEY autoincrement,
   user       CHAR(120),
   pwd        CHAR(120),
   url        TEXT,
   status     int,
   saved      int,
   task_id    CHAR(50),
   file       TEXT,
  update_time DATETIME

);
"""


class Download(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120), unique=False)
    pwd = db.Column(db.String(120), unique=False)
    url = db.Column(db.TEXT, unique=False)
    status = db.Column(db.Integer, unique=False)  # 0,1,2 未完成 已完成 失败
    saved = db.Column(db.Integer, unique=False)  # 0, 1, 2 未下载 已下载 已删除
    task_id = db.Column(db.String(500), unique=True)
    file = db.Column(db.String(510), unique=True)
    update_time = db.Column(db.DateTime, unique=False)

    def __init__(self, user, pwd, url, task_id, file='', status=0, saved=0, update_time=datetime.now()):
        self.user = user
        self.pwd = pwd
        self.url = url
        self.task_id = task_id
        self.status = status
        self.saved = saved
        self.update_time = update_time
        self.file = task_id + file

    def __repr__(self):
        return '<task %r>' % self.task_id
# 创建表格、插入数据
