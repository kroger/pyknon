.PHONY: coverage test coverage docs

test:
	py.test

coverage:
	py.test --cov=pyknon --cov-report=html

check:
	pylint pyknon

docs:
	cd docs && make html

view: docs
	open docs/_build/html/index.html

clean:
	find . -name "*.pyc" | xargs rm -f
	find . -name "__pycache__" | xargs rm -rf
	rm -rf .cache .coverage htmlcov

cleanall: clean
	rm -rf htmlcov docs/_build
