release: python Web/manage.py migrate && python Bot/scripts.py
web: gunicorn --pythonpath Web LeetcodeTracker.wsgi
worker: python Bot/main.py

# release spins a dyno to perform a web migration, this dyno is removed once the migration is completed.
# web routes traffic to the django application located in Web/LeetcodeTracker/wsgi.py
# worker spins up the discord bot.

# If you intend on running the bot 24/7 and also anticipate a lot of web traffic it's reccomended to run the web process
# on a hobby dyno and the worker on a free dyno to best utilize funds.

# IMPORTANT:
# If you intend on using Azure SQL you'll need to configure your dyno with the proper buildpacks. Follow the
# instructions in this github repository : https://github.com/matt-bertoncello/python-pyodbc-buildpack
