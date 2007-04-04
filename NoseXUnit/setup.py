#-*- coding: utf-8 -*-
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(
	name="NoseXUnit",
	version="0.1",
	description="XML Output plugin for Nose",
	long_description="A plugin for nose/nosetests that produces an XML report of the result of a test.",
	author="Mansion Olivier",
	author_email="nosexunit@gmail.com",
	packages=['nosexunit'],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Programming Language :: Python',
		'Topic :: Communications :: Email',
		'Topic :: Office/Business',
		'Topic :: Software Development :: Testing',
		],
	entry_points = {'nose.plugins': [ 'nosexunit = nosexunit.plugin:NoseXUnit' ] },
        test_suite = 'nose.collector',
	)
