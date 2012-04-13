.PHONY: coverage tests cov doc

test:
	py.test

coverage:
	py.test --cov=pyknon --cov-report=html

doc:
	cd doc && make html

view: doc
	open doc/_build/html/index.html

clean:
	find . -name "*.pyc" | xargs rm

