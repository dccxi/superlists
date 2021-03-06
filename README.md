## Introduction
Superlists is a todo-list web app featuring:
- Passwordless Login using only email
- Save separate todo lists for logged in user
- Access saved todo lists using URL for anonymous users

Feel free to check it out at: https://superlists.dccxi.com

It's a practice project I built during the summer of 2019 while learning Django, Linux, and Web Development as well as TDD methodology in general.

The most of the parts in the project was following the first 23 out of 26 chapters of the book *Test-Driven Development with Python, 2e* by Harry Percival. It's a very thoughtful book with smooth learning curve, definitely worth your time if you are curious about TDD or simply want to try out Django for web development.

Over the course of building this project, I gained a better understanding of the following subjects:
- Django Framework
- Python Language
    - LEGB Scoping
    - Runtime Dynamic Linking
    - Application of Decorators
    - OOP and FP Styles
- Server Provisioning
    - Automated Provisioning using Ansible and/or Fabric
    - Nginx Configuration
- Testing
    - Mocking
    - Unit Tests
    - Functional Tests
    - Integration Tests between Layers (ex. view and model)
- etc.

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
$ R_USER=deploy_user
$ R_HOST=example.com
$ cd deploy_tools
$ EMAIL_PASSWORD={} # replace {} with SMTP password of your own email
$ fab deploy:sitename={},email_password=$EMAIL_PASSWORD,host=$R_USER@$R_HOST # replace {} with your own domain name
```

### Running Functional Tests against Staging Server before Production
```shell
$ EMAIL_PASSWORD={} # replace {} with SMTP password of your own email
$ STAGING_SERVER={} # replace {} with your own staging server ** domain name **
$ remote_host={}    # replace {} with your own staging server ** IP **
$ python manage.py test functional_tests
$ # remember to unset the STAGING_SERVER variable otherwise local FT will fail
$ unset STAGING_SERVER
```
or to avoid using `unset`:
```shell
$ STAGING_SERVER={} EMAIL_PASSWORD={} remote_host={} python manage.py test functional_tests
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
