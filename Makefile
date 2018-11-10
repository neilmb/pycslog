.PHONY: test
test: pytest lint

pytest:
	py.test --cov=pycslog --cov-report term-missing test/

lint:
	pylint pycslog run_cmd_client.py setup.py
