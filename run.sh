# kill already running instance first
kill -9 `cat /var/run/easy_todo.pid`
./env/bin/gunicorn -c easy_todo/config/prod.py
