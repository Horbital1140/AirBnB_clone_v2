#!/usr/bin/python3
from fabric.api import run, local, task, lcd, cd, put
from os import listdir, path
from datetime import datetime as stamp
from hosts import *


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
        run("tar -xzf /tmp/{}.tgz -C {}/{}".format(web_static, releases,
                                                   web_static))
        run("rm /tmp/{}.tgz".format(web_static))
        run("mv {0}/{1}/web_static/* {0}/{1}/".format(releases, web_static))
        run("rm -rf {}/{}/web_static".format(releases, web_static))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/{}/ /data/web_static/current".format(releases,
                                                           web_static))
        print("New version deployed!")
        return True
    except Exception:
        return False


@task
def deploy():
    """Full deployment to cloud"""
    archive = do_pack()

    if not archive:
        return False

    return do_deploy(archive)


@task(alias="clean")
def do_clean(number=0):
    """A cleanup function to delete old releases"""
    files = listdir("./versions")
    files = sorted(files)[::-1]
    number = 1 if int(number) == 0 else int(number)
    with lcd("versions"):
        for file in files[number:]:
            local("rm -f {}".format(file))

    with cd("/data/web_static/releases"):
        re = sorted(list(filter(lambda x: "web_static_" in x,
                                run("ls").split())))[::-1]
        for file in re[number:]:
            run("rm -rf {}".format(file))
