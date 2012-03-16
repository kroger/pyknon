.PHONY: coverage tests cov

test:
	py.test

coverage:
	py.test --cov=pyknon --cov-report=html
