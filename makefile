migrate:
	python manage.py makemigrations
	python manage.py migrate
dev:
	python manage.py runserver
installrequirements:
	pip install -r requirements.txt
addrequirements:
	pip freeze > requirements.txt
