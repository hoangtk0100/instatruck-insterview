install:
	pip install -r requirements.txt 

server:
	python3 manage.py runserver 0.0.0.0:8000

migrate:
	python3 manage.py migrate

makemigrations:
	python3 manage.py makemigrations

initdata:
	python3 manage.py initialize_data

initdb:
	python3 manage.py loaddata initial_database.json

backupdb:
	python3 manage.py dumpdata --indent 2 > database_backup.json

restoredb:
	python3 manage.py loaddata database_backup.json

createsuperuser:
	python3 manage.py createsuperuser

.PHONY: install server migrate makemigrations initdata initdb backupdb restoredb createsuperuser