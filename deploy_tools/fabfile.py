from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = "https://dccxi@bitbucket.org/dccxi/superlists.git"


def deploy(sitename, live="True"):
    site_folder = f"/home/{env.user}/sites/{sitename}"
    source_folder = site_folder + "/source"
    _crete_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, sitename)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    if live == "True":
        _deploy_to_live(source_folder, sitename)


def _crete_directory_structure_if_necessary(site_folder):
    for subfolder in ("database", "static", "virtualenv", "source"):
        run(f"mkdir -p {site_folder}/{subfolder}")


def _get_latest_source(source_folder):
    if exists(source_folder + "/.git"):
        run(f"cd {source_folder} && git fetch")
    else:
        run(f"git clone {REPO_URL} {source_folder}")
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"cd {source_folder} && git reset --hard {current_commit}")


def _update_settings(source_folder, site_name):
    settings_path = source_folder + "/superlists/settings.py"
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, "ALLOWED_HOSTS =.+$", f'ALLOWED_HOSTS = ["{site_name}"]')
    secret_key_file = source_folder + "/superlists/secret_key.py"
    if not exists(secret_key_file):
        chars = (
            "".join([chr(i) for i in range(97, 123)])
            + "".join([chr(i) for i in range(48, 58)])
            + "!@#$%^&*(-_=+)"
        )
        # generate new keys for production
        # so that it's not duplicated with the source
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, "\nfrom .secret_key import SECRET_KEY")


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + "/../virtualenv"
    if not exists(virtualenv_folder + "/bin/pip"):
        run(f"python3 -m venv {virtualenv_folder}")
    run(f"{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt")


def _update_static_files(source_folder):
    run(
        f"cd {source_folder}"
        " && ../virtualenv/bin/python manage.py collectstatic --noinput"
    )


def _update_database(source_folder):
    run(f"cd {source_folder} && ../virtualenv/bin/python manage.py migrate --noinput")


def _deploy_to_live(source_folder, site_name):
    run(
        f"cd {source_folder}"
        f' && sed "s/SITENAME/{site_name}/g" deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/{site_name}'
        f" && sudo ln -sf ../sites-available/{site_name} /etc/nginx/sites-enabled/{site_name}"
        f' && sed "s/SITENAME/{site_name}/g" deploy_tools/gunicorn-systemd.template.service | sudo tee /etc/systemd/system/gunicorn-{site_name}.service'
        " && sudo systemctl daemon-reload"
        " && sudo systemctl reload nginx"
        f" && sudo systemctl enable gunicorn-{site_name}"
        f" && sudo systemctl start gunicorn-{site_name}"
    )
