#-*- coding: utf-8 -*-
import sys
import distutils.util

if sys.version_info[0] > 2 or (sys.version_info[0] == 2 and sys.version_info[1] >= 5):
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
else:
    import warnings
    warnings.warn('setuptools not used')
    from distutils.core import setup

execfile(distutils.util.convert_path('paradox/__init__.py'))

setup(
    name = "Paradox",
    version = __version__,
    description = "Get reports on NoseXUnit tests",
    long_description = "How to get NoseXUnit reports without NoseXUnit? That is the point!",
    author = "Olivier Mansion",
    author_email = "nosexunit@gmail.com",
    license = "GNU Library or Lesser General Public License (LGPL)",
    url = "http://nosexunit.sourceforge.net",
    packages = ['paradox'],
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
    install_requires = ['nose >= 0.10.4', ],
    entry_points = {'nose.plugins.0.10': [ 'paradox = paradox.plugin:Paradox' ] },
    test_suite = 'nose.collector',
)

