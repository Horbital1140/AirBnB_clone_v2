#!/usr/bin/python3
""" This module is used to deploy static files to cloud """
from fabric.api import task, local, run, env, put, hosts, runs_once
from datetime import datetime as stamp
from os import path
from hosts import *


@task
@runs_once
def do_pack():
    """Function that returns a gzip compressed file"""
    try:
        time_stamp = stamp.now().strftime("%Y%m%d%H%M%S")
        __path = f"versions/web_static_{time_stamp}.tgz"
        local("mkdir -p versions")
        local(f"tar -cvzf {__path} web_static")
    except Exception:
        return None
    else:
        return __path


@task
def do_deploy(archive_path):
    """Function distributes an archive to my web servers"""
    if not path.exists(archive_path):
        return False

    releases = "/data/web_static/releases"
    if put(archive_path, "/tmp/").failed:
        return False

    web_static = path.basename(archive_path).split(".")[0]
    mkdir_command = "mkdir -p {}/{}".format(releases, web_static)
    if run(mkdir_command).failed:
        return False

    tar_command = "tar -xzf /tmp/{}.tgz -C {}/{} --strip-components=1".format(
        web_static, releases, web_static
    )
    if run(tar_command).failed:
        return False

    rm_archive_command = "rm -f /tmp/{}.tgz".format(web_static)
    if run(rm_archive_command).failed:
        return False

    rm_current_command = "rm -rf /data/web_static/current"
    if run(rm_current_command).failed:
        return False

    ln_command = "ln -sf {}/{} /data/web_static/current".format(releases,
                                                                web_static)
    if run(ln_command).failed:
        return False

    return True

@task
def deploy():
    """Full deployment to cloud"""
    archive = do_pack()

    if not archive:
        return False

    return do_deploy(archive)
