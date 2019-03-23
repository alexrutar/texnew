from setuptools import setup, find_packages
from texnew import __version__
def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='texnew',
    version=__version__,
    description='An automatic LaTeX template creator and manager.',
    long_description=readme(),
    url='https://github.com/alexrutar/texnew',
    author='Alex Rutar',
    author_email='arutar@uwaterloo.ca',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License'
        ],
    keywords='LaTeX template',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'pyyaml>=3.13'
        ],
    include_package_data=True,
    entry_points={'console_scripts': ['texnew = texnew.__main__:main']},
    zip_safe=False
    )

