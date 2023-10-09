#!/usr/bin/python3
"""Fabric script that compresses my static files with gzip """

from fabric.api import task, local
from datetime import datetime as stamp


@task(alias="pack")
def do_pack():
    """Function that returns a gzip compressed file"""
    try:
        time_stamp = stamp.now().strftime('%Y%m%d%H%M%S')
        path = "versions/web_static_{}.tgz".format(time_stamp)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(path))
    except Exception:
        return None
    else:
        return path
