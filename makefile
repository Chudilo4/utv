migrate:
	python manage.py makemigrations
	python manage.py migrate
dev:
	python manage.py runserver
installrequirements:
	pip install -r requirements.txt
addrequirements:
	pip freeze > requirements.txt
addbuilddocker:
	docker build -t utv .
rundockerbuild:
	docker run -it utv
httpsdev:
	python manage.py runsslserver --certificate cert.pem --key key.pem
