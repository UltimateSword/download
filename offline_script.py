from urllib.parse import urlparse
from models import db, Download
import os
from utils import disk_usage


def download():
    tasks = Download.query.filter_by(status=0).all()
    for t in tasks:
        percent = disk_usage('/').percent
        if percent > 95:
            continue
        domain = urlparse(t.uri).netloc
        # ParseResult(scheme='https', netloc='www.baidu.com', path='/', params='', query='', fragment='')
        if 'youtubue' in domain:
            continue
        else:
            rep = os.system('wget -u {} -user {} -password {}'.format(t.url, t.user, t.password))
            if rep == 0:
                t.status = 1
            else:
                t.status = 2
    db.session.commit()

