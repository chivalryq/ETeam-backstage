pkill gunicorn
cd /var/www/eteam
source eteam-env/bin/activate
gunicorn run:app  -b 0.0.0.0:5000 -w 4 --worker-class gevent
deactive