release: python Web/manage.py migrate && python Bot/main.py
web: gunicorn --pythonpath Web LeetcodeTracker.wsgi