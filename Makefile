pipenv:
	python3 -m venv .venv
	./.venv/bin/pip install --upgrade pip setuptools
	./.venv/bin/pip install pipenv

requirements-dev: pipenv
	./.venv/bin/pipenv install --dev

clean:
	-rm -r .venv dist build src/*.egg-info
