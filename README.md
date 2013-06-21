mro
===

* ADD DEPENDENCIES
** Change to your local virtual env
source venv/bin/activate

** Install them with pip
pip install PUT_NAME_HERE

** Add them to requirements.txt using the proper version number
echo 'PUT_NAME_HERE==PUT_VERSION_HERE' >> requirements.txt

* HOW TO RUN LOCALLY
** Database
Create a user called 'myrunningorder' with password 'ficken'
Create a database called 'myrunningorder_dev'

** Static Files
Every time you add static files you need to run the following command before being able to see them on your local web server
python manage.py collectstatic

** Local Web Server
foreman start

* DATABASE MIGRATIONS
** Local
python manage.py syncdb

** Heroku
heroku run python manage.py syncdb
