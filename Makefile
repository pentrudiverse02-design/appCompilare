.PHONY: server client run-clients run-server clean 
SHELL := bash

server: comunee
	ls
	source env/bin/activate &&\
	python3 serverdir/*.py
comunee:
	# aici trebuie verificate daca compileaza ok fiecare comune
	python3 -m venv env &&\
	source env/bin/activate &&\
	cd comune &&\
	python3 *.py
