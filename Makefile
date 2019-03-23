test:
	python3 -m texnew -c
upload:
	-/usr/local/bin/python3 setup.py register sdist upload
