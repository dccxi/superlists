## Deployment Process
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
