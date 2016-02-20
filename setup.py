#!/usr/bin/env python

import os.path
import fireplace
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import call

README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

CLASSIFIERS = [
	"Development Status :: 2 - Pre-Alpha",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)"
	"Programming Language :: Python",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.5",
	"Topic :: Games/Entertainment :: Simulation",
]


def post_install(install_dir):
	call(os.path.join(os.path.curdir, "bootstrap"),
		 cwd=os.path.join(install_dir, "fireplace"),
		 shell=True)


class custom_install(install):
	def run(self):
		super(custom_install, self).run()
		self.execute(post_install, [self.install_lib],
					 msg="Running card definition bootstrap")


class custom_develop(develop):
	def run(self):
		super(custom_develop, self).run()
		self.execute(post_install, [self.setup_path],
					 msg="Running card definition bootstrap")


tests_require=["pytest"]
setup(
	name="fireplace",
	version=fireplace.__version__,
	packages=find_packages(exclude="tests"),
	package_data={"fireplace":["bootstrap", "scripts/bootstrap.*"]},
	include_package_data=True,
	tests_require=tests_require,
	extras_require={
		'test': tests_require,
	},
	install_requires=["hearthstone"],
	dependency_links=["git+https://github.com/HearthSim/python-hearthstone.git#egg=hearthstone-0"],
	cmdclass={"develop":custom_develop,
			  "install":custom_install},
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
