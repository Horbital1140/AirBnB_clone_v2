from fabric.api import task, local
from datetime import datetime as stamp


@task(alias="pack")
def do_pack():
    """Function that returns a gzip compressed file"""
    try:
        time_stamp = stamp.now().strftime('%Y%m%d%H%M%S')
        path = f"versions/webstatic{time_stamp}.tgz"
        local("mkdir -p versions")
        local(f"tar -cvzf {path} web_static")
    except Exception:
        return None
    else:
        return path
