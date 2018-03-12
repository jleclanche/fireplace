#!/usr/bin/env python

import fireplace
from setuptools import setup, find_packages


CLASSIFIERS = [
	"Development Status :: 2 - Pre-Alpha",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)"
	"Programming Language :: Python",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.6",
	"Topic :: Games/Entertainment :: Simulation",
]

tests_require = ["pytest", "pytest-benchmark[aspect]"]

setup(
	name="fireplace",
	version=fireplace.__version__,
	packages=find_packages(exclude="tests"),
	install_requires=["hearthstone"],
	tests_require=[tests_require],
	extras_require={"tests": tests_require},
	author=fireplace.__author__,
	author_email=fireplace.__email__,
	description="Pure-python Hearthstone re-implementation and simulator",
	classifiers=CLASSIFIERS,
	download_url="https://github.com/jleclanche/fireplace/tarball/master",
	license="AGPLv3",
	url="https://github.com/jleclanche/fireplace",
	zip_safe=True,
)
