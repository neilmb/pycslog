.PHONY: test
test: nose lint

nose:
	nosetests --with-coverage

lint:
	prospector -M
