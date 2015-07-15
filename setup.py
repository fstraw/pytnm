try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'Analysis of FHWA\'s TNM 2.5 Outputs',
	'author': 'Brandon Batt',
	'url': 'www.lowestfrequency.com',
	'download_url': 'www.lowestfrequency.com',
	'author_email': 'fstraw@lowestfrequency.com',
	'version': '0.1',
	'install_requires': ['openpyxl'],
	'tests_require': ['nose']
	'packages': ['pytnm'],
	'scripts': [],
	'name': 'pytnm'
}

setup(**config)