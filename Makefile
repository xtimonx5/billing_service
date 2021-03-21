_python = python3
_manage_py = $(_python) manage.py
_pip = pip3
_pipenv = pipenv
_execc = docker-compose exec
_runc = docker-compose run
_pytest = python3 -B -m pytest

###############################################################################
#
# PIPenv related
#
###############################################################################

pipenv_graph:
	$(_execc) app $(_pipenv) graph

pipenv_check:
	$(_execc) app $(_pipenv) check

pipenv_install:
	$(_execc) app $(_pipenv) install $(PIP_PACKAGE)

pipenv_uninstall:
	$(_execc) app $(_pipenv) uninstall $(PIP_PACKAGE)

pipenv_actualize:
	$(_execc) app $(_pipenv) install --deploy

pipenv_lock:
	$(_execc) app $(_pipenv) lock

###############################################################################
#
# OS related
#
###############################################################################
app_bash:
	$(_execc) app bash


###############################################################################
#
# Docker related
#
###############################################################################
build:
	docker-compose build

up:
	docker-compose up

up_app:
	docker-compose up app

###############################################################################
#
# Django related
#
###############################################################################

launch:
	$(_execc) app $(_manage_py) runserver 0.0.0.0:8000

startapp:
	$(_execc) app $(_manage_py) startapp $(APP)

check:
	$(_execc) app $(_manage_py) check

migrate:
	$(_execc) app $(_manage_py) migrate

shell:
	$(_execc) app $(_manage_py) shell

migration:
	$(_execc) app $(_manage_py) makemigrations

migration_merge:
	$(_execc) app $(_manage_py) makemigrations --merge

compile_message_all:
	$(_runc) app python manage.py compilemessages --locale ae --locale by --locale cz --locale de --locale en --locale es --locale fr --locale gb --locale in --locale it --locale kz --locale pl --locale pt --locale ru --locale tr --locale uk


###############################################################################
#
# Unit Testing related
#
###############################################################################

clean_before_test:
	@find ./ -name '*.pyc' -delete

test: clean_before_test
	$(_execc) app $(_pytest)

linter: clean_before_test
	$(_execc) app bash -c 'find . -name "*.py" | xargs pylint'

coverage:
	$(_execc) app $(_pytest) --cov='.'

coverage_html:
	$(_execc) app $(_pytest) --cov='.' --cov-report html

