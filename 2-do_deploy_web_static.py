#!/usr/bin/python3
"""
Distribute an archive to web servers using Fabric.
"""

from fabric.api import run, local, put, task
from os import path
from datetime import datetime as stamp
from hosts import *  # Make sure you import your host configuration here.

@task
def do_pack():
    """Create a compressed archive of the 'web_static' directory."""try:
	time_stamp = stamp.now().strftime("%Y%m%d%H%M%S")
	archive_path = f"versions/web_static_{time_stamp}.tgz"
	
	local("mkdir -p versions")
	local(f"tar -cvzf {archive_path} web_static")

	return archive_path
except Exception as a:
	print(f"Error while creating archive: {a}")
	return None

@task
def do_deploy(archive_path):
    """Distribute an archive to web servers and update the deployment."""

try:
        if not path.exists(archive_path):
		print(f"Archive not found: {archive_path}")
		return False
	releases_dir = "/data/web_static/releases"
        archive_name = path.basename(archive_path).split(".")[0]
	put(archive_path, "/tmp/")
	run(f"rm -rf {releases_dir}/{archive_name}")
        
        run(f"mkdir -p {releases_dir}/{archive_name}")
        
        run(f"tar -xzf /tmp/{archive_name}.tgz -C {releases_dir}/{archive_name}")
        
        run(f"rm /tmp/{archive_name}.tgz")
	run(f"mv {releases_dir}/{archive_name}/web_static/* {releases_dir}/{archive_name}/")
       
        run(f"rm -rf {releases_dir}/{archive_name}/web_static")
        
        
        run(f"ln -s {releases_dir}/{archive_name} /data/web_static/current")

        print("New version deployed successfully!")
        return True
    except Exception as e:
        print(f"Error while deploying: {a}")
        return False
