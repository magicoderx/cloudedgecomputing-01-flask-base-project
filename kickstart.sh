#!/bin/sh

export FLASK_APP=app.py
flask db init
flask db migrate
flask db upgrade

if [ "$RUN_TESTS" = "true" ]; then
    exec python test_http.py  
else
    exec gunicorn -w 4 -b 0.0.0.0:8080 wsgi:app
fi