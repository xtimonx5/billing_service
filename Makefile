_python = python3
_manage_py = $(_python) manage.py
_execc = docker-compose exec
_pytest = python3 -B -m pytest

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

###############################################################################
#
# Django related
#
###############################################################################

launch:
	$(_execc) app $(_manage_py) runserver 0.0.0.0:8000


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

