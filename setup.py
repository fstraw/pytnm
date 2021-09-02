import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="pytnm",
    version="1.1",
    description="FHWA TNM 2.5 Geospatial Toolkit",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/fstraw/pytnm",
    author="Brandon Batt",
    author_email="brbatt@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=[
		"pytnm",
		"pytnm.utils",
		"pytnm.utils.report"
	],
    install_requires=["openpyxl", "pyshp"],
)