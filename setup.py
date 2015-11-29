#!/usr/bin/env python

import os.path
import fireplace
from setuptools import setup, find_packages


README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

CLASSIFIERS = [
	"Development Status :: 2 - Pre-Alpha",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)"
	"Programming Language :: Python",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.4",
	"Topic :: Games/Entertainment :: Simulation",
]

setup(
	name="fireplace",
	version=fireplace.__version__,
	packages=find_packages(exclude="tests"),
	package_data={"": ["CardDefs.xml"]},
	include_package_data=True,
	tests_require=["pytest"],
	author=fireplace.__author__,
	author_email=fireplace.__email__,
	description="Pure-python Hearthstone re-implementation and simulator",
	classifiers=CLASSIFIERS,
	download_url="https://github.com/jleclanche/python-bna/tarball/master",
	long_description=README,
	license="AGPLv3",
	url="https://github.com/jleclanche/fireplace",
)
