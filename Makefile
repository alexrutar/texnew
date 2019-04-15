.PHONY: upload test longtest
test:
	-trash test/*
	-python3 -m texnew new test/test.tex asgn
	-echo "extra text" >> test/test.tex
	-python3 -m texnew -v update test/test.tex notes -t doctype
	-python3 -m texnew info -ld
	-python3 -m texnew --version
upload:
	-pandoc --from=markdown --to=rst --output=README.rst short_description.md
	-/usr/local/bin/python3 setup.py sdist bdist_wheel
	-twine upload dist/*
longtest: test
	-python3 -m texnew check asgn
	-python3 -m texnew check --all
