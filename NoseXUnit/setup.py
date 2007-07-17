#-*- coding: utf-8 -*-
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

setup(
    name="NoseXUnit",
    version="0.2.0a1",
    description="XML Output plugin for Nose",
    long_description="A plugin for nose/nosetests that produces an XML report of the result of a test.",
    author="Olivier Mansion",
    author_email="nosexunit@gmail.com",
    packages=['nosexunit'],
    classifiers=[
        'Development Status: 2 - Pre-Alpha',
        'Intended Audience: Developers, Quality Engineers',
        'License: Public Domain',
        'Operating System: All POSIX (Linux/BSD/UNIX-like OSes)',
        'Programming Language: Python',
        'Topic: Testing',
        'Translations: English',
        'User Interface: Plugins',
        ],
    install_requires = [ "nose == 0.10.0a1", ],
    entry_points = {'nose.plugins': [ 'nosexunit = nosexunit.plugin:NoseXUnit' ] },
    test_suite = 'nose.collector',
)
