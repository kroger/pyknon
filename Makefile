.PHONY: coverage test coverage docs

test:
	py.test

coverage:
	py.test --cov=pyknon --cov-report=html

docs:
	cd docs && make html

view: docs
	open docs/_build/html/index.html

clean:
	find . -name "*.pyc" | xargs rm

cleanall: clean
	rm -rf htmlcov docs/_build

