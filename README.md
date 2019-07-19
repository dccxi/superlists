## Deployment Process (nonautomated)
On remote server:
* Provisioning
    * Create or add a new user account in sudo group, and home folder
        * `$ useradd -m -s /bin/bash elspeth`
        * `$ passwd elspeth`
        * `$ usermod -aG sudo elspeth`
    * Verify
        * `$ su - elspeth`
        * `$ id elspeth`
        * `$ logout`
    * Set up ssh only access for security
    * Install nginx git python3.6+
    * Add nginx config file for virtual host
        * `$ sudo nginx -t`
        * `$ sudo nginx -s reload`
    * Add Systemd job for Gunicorn
        * `$ sudo systemctl daemon-reload`
        * `$ sudo systemctl enable gunicorn-SITENAME`
        * `$ sudo systemctl start gunicorn-SITENAME`
* Deployment
    * Create directory structure in ~/sites
        * ~/sites/SITENAME/source
        * ~/sites/SITENAME/static
        * ~/sites/SITENAME/database
        * ~/sites/SITENAME/virtualenv
            * `$ python3 -m venv`
    * Pull source code
    * Start venv in ../virtualenv
    * In venv, `$ pip install -r requirements.txt`
    * `$ manage.py migrate` for database
    * `$ manage.py collectstatic` for static files
    * Restart Gunicorn
    * Run FT to check

## Deployment Process (automated)
On local machine:
```shell
$ pip3 install fabric3
```

Make sure `~/.local` is in `PATH`, and `~/.ssh` exists, then:

``` shell
$ USER=deploy_user
$ HOST=example.com
$ cd deploy_tools
$ fab deploy:sitename=superlists.dccxi.com,host=$USER@$HOST
```

## Provisioning with Ansible (before deployment)
Using a local Vagrant VM running Ubuntu 19.04 for example.

Before proceed, initialize a `bento/ubuntu-19.04` Vagrant VM and expose port 80 from guest to host's port 8080 using `Vagrantfile`.

Built `inventory.ansible` and `provision.ansible.yaml` first, then:

```shell
$ pip3 install ansible
$ ansible-playbook -i inventory.ansible provision.ansible.yaml --limit=local
 --ask-become-pass
# deployment is not configured yet, use fabric3 script
$ fab deploy:sitename=localhost,live=False,host=vagrant@localhost:2222
```

Now navigate to `localhost:8080`, the server should be running properly
