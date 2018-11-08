.PHONY: test
test: nose lint

nose:
	nosetests --with-coverage

lint:
	pylint pycslog run_cmd_client.py setup.py
