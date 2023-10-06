#!/usr/bin/python3
"""Fabric script that compresses my static files with gzip """

from fabric.api import task, local
from datetime import datetime as stamp


@task(alias="tasky")
def do_pack():
	"""this function returns gzip compresed file"""
	try:
		time_stamp = stamp.now().strftime('%Y%m%d%H%M%S')
		path = f"versions/web_static_{time_stamp}.tgz"
		local("mkdir -p versions")
		local(f"tar -cvzf {path} web_static")
		return path
	except Exception:
		return None
