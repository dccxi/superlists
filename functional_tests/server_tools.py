import os
from fabric.api import run
from fabric.context_managers import settings


def _get_manage_dot_py(sitename):
    return f"~/sites/{sitename}/virtualenv/bin/python ~/sites/{sitename}/source/manage.py"

def reset_database(sitename):
    manage_dot_py = _get_manage_dot_py(sitename)
    with settings(host_string=f"elspeth@{os.environ['remote_host']}"):
        run(f"{manage_dot_py} flush --noinput")

def create_session_on_server(sitename, email):
    manage_dot_py = _get_manage_dot_py(sitename)
    with settings(host_string=f"elspeth@{os.environ['remote_host']}"):
        session_key = run(f"{manage_dot_py} create_session {email}")
        return session_key.strip()
