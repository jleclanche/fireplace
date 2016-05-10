#!/usr/bin/env python

import os.path
import fireplace
from setuptools import setup, find_packages

_basedir = os.path.dirname(__file__)
README = open(os.path.join(_basedir, "README.md")).read()
with open(os.path.join(_basedir, "requirements.txt")) as f:
	requirements = f.read().splitlines()

CLASSIFIERS = [
	"Development Status :: 2 - Pre-Alpha",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)"
	"Programming Language :: Python",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.5",
	"Topic :: Games/Entertainment :: Simulation",
]

tests_require = ["pytest", "pytest-benchmark[aspect]"]

setup(
	name="fireplace",
	version=fireplace.__version__,
	packages=find_packages(exclude="tests"),
	install_requires=requirements,
	tests_require=[tests_require],
	extras_require={"tests": tests_require},
	author=fireplace.__author__,
	author_email=fireplace.__email__,
	description="Pure-python Hearthstone re-implementation and simulator",
	classifiers=CLASSIFIERS,
	download_url="https://github.com/jleclanche/fireplace/tarball/master",
	long_description=README,
	license="AGPLv3",
	url="https://github.com/jleclanche/fireplace",
	zip_safe=True,
)
