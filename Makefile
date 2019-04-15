.PHONY: upload test longtest
test:
	-trash test/*
	-python3 -m texnew new test/test.tex asgn
	-python3 -m texnew update test/test.tex notes
upload:
	-pandoc --from=markdown --to=rst --output=README.rst short_description.md
	-/usr/local/bin/python3 setup.py sdist bdist_wheel
	-twine upload dist/*
longtest: test
	-python3 -m texnew check --all
