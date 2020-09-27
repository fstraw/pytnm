try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'FHWA\'s TNM 2.5 Toolkit',
	'author': 'Brandon Batt',		
	'author_email': 'brbatt@gmail.com',
	'version': '0.5',
	'install_requires': ['openpyxl'],
	'tests_require': ['pytest'],
	'packages': ['pytnm'],
	'package_dir': {'pytnm': 'pytnm'},
	'scripts': [],
	'name': 'pytnm'
}

setup(**config)