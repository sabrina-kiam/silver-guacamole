Provisioning a new site:
========================

##  Required packages:
* nginx
* python3.8
* vitualenv + pip
* git

eg on Ubuntu:
	sudo add-apt-respository ppa:deadsnakes/ppa
	sudo apt update
	sudo apt install nginx git python36 python3.6-venv

## Nginx virtual host config
* see nginx.template.conf
* replace DOMAIN with e.g. staging.my-domain.com

## Systemd service
* see gunicorn-systemd.template.service
* replace DOMAIN with e.g. staging.my-domain.com

## Folder structure
Assume we have a user account at /home/username
Within username should be a directory sites.
Sites should contain a folder or each site, which should contain:
.env, db.sqlite3, manage.py etc, static, and virtualenv files