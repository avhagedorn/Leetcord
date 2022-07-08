release: python Web/manage.py migrate
web: gunicorn --pythonpath Web LeetcodeTracker.wsgi
worker: python Bot/main.py