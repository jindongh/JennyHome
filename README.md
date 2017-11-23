# Jenny's Home
* Garage
* Reminder
* Note

# Environment
```
sudo apt-get install python-opencv python-dev
virtualenv env
source env/bin/activate
pip install -r requirements.txt
pip install git+https://github.com/jindongh/django-apscheduler.git
cp /usr/bin/python2.7/dist-packages/cv* env/lib/python2.7/site-packages

```
# Get Started
```
virtualenv env
source env/bin/activate
# grant permission for dhcp detection.
sudo setcap cap_net_raw,cap_net_admin=eip $(which python2)
./start
```

# Development
```
python manage.py test garage
```
