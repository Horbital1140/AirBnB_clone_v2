#!/usr/bin/python3
""" Distributes an archive to my web servers """
from fabric.api import run, local, put, task, env
from os import path
from datetime import datetime as stamp


env.hosts = ["100.25.188.129", "204.236.240.90"]


@task(alias="pack")
def do_pack():
    """Function that returns a gzip compressed file"""
    try:
        time_stamp = stamp.now().strftime('%Y%m%d%H%M%S')
        __path = "versions/web_static_{}.tgz".format(time_stamp)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(__path))
    except Exception:
        return None
    else:
        return __path


@task
def do_deploy(archive_path):
    """Function distributes an archive to my web servers"""
    try:
        if not path.exists(archive_path):
            return False

        releases = "/data/web_static/releases"
        web_static = path.basename(archive_path).split(".")[0]
        put(archive_path, "/tmp/")
        run("rm -rf {}/{}/".format(releases, web_static))
        run("mkdir -p {}/{}/".format(releases, web_static))
        run("tar -xzf /tmp/{}.tgz -C {}/{}".format(web_static,
                                                   releases,
                                                   web_static))
        run("rm /tmp/{}.tgz".format(web_static))
        run("mv {0}/{1}/web_static/* {0}/{1}/".format(releases,
                                                      web_static))
        run("rm -rf {}/{}/web_static".format(releases,
                                             web_static))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/{}/ /data/web_static/current".format(releases,
                                                           web_static))
        print("New version deployed!")
        return True
    except Exception:
        return False
