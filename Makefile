.PHONY: test
test: nose lint

nose:
	nosetests --with-coverage

lint:
	pylint pycslog run_cmd_client.py run_server.py setup.py
