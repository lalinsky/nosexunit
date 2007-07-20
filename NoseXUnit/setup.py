#-*- coding: utf-8 -*-
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

setup(
    name = "NoseXUnit",
    version = "0.2.0c1",
    description = "XML Output plugin for Nose",
    long_description = "A plugin for nose/nosetests that produces an XML report of the result of a test.",
    author = "Olivier Mansion",
    author_email = "nosexunit@gmail.com",
    license = "GNU Library or Lesser General Public License (LGPL)",
    url = "http://nosexunit.sourceforge.net",
    packages = ['nosexunit'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        ],
    install_requires = ['nose >= 0.10.0a2', ],
    entry_points = {'nose.plugins.0.10': [ 'nosexunit = nosexunit.plugin:NoseXUnit' ] },
    test_suite = 'nose.collector',
)

