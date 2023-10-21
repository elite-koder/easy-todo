"""Gunicorn *development* config file"""
import os

wsgi_app = "easy_todo.wsgi:application"
log_level = "debug"
workers = 1
bind = "localhost:8000"
accesslog = errorlog = "/var/log/easy_todo/default"
capture_output = True
pidfile = "/var/run/easy_todo.pid"
daemon = True
raw_env = ["FABRIC=PROD"]
