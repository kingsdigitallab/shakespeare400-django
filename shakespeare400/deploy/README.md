# Django Deployment with uWSGI

## uWSGI

Install uWSGI into the system Python libraries
```
sudo pip install uwsgi
```

Create a uWSGI configuration for the project:
```
[uwsgi]

# django-related settings
# absolute path to the project directory
chdir = /vagrant
# path to the project wsgi file, relative to the project directory
wsgi-file = shakespeare400/wsgi.py
# absolute path to the project virtual environment
home = /home/vagrant/venv

# process-related settings
# master
master = true
# maximum number of worker processes
processes = 1
# absolute path to the socket
socket = /tmp/shakespeare400.sock
# ... with appropriate permissions - may be needed
chmod-socket = 666
# clear environment on exit
vacuum = true
```

Set up uWSGI to run in **emperor** mode, to watch a directory of uWSGI configuration files and spawn instances (vassals) for each one it finds. Whenever a configuration file changes, the emperor automatically restarts the vassal.
```
# create a directory for the vassals
sudo mkdir -p /etc/uwsgi/vassals
# create a link from the default config directory to the project config file
sudo ln -s /path/to/the/project/project_uwsgi.ini /etc/uwsgi/vassals/
# run the emperor
sudo uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data 
```

To start the emperor when the system starts edit `/etc/rc.local` and add:
```
/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /var/log/uwsgi-emperor.log
```

Before the line `exit 0`.

## Apache
[Apache with uWSGI](https://uwsgi.readthedocs.org/en/latest/Apache.html)

## nginx
[nginx with uWSGI](https://uwsgi.readthedocs.org/en/latest/tutorials/Django_and_nginx.html)
