test:
	-python3 -m texnew -c
upload:
	-pandoc --from=markdown --to=rst --output=README.rst README.md
	-/usr/local/bin/python3 setup.py sdist bdist_wheel
	-twine upload dist/*
