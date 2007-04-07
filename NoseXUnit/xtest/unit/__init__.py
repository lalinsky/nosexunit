#-*- coding: utf-8 -*-
import os
import sys

# Get the absolute path of the folder containing this file
absfld = os.path.dirname(os.path.abspath(__file__))

# Get the folder containing the plugin module
plugfld = os.path.normpath(os.path.join(absfld, os.path.pardir, os.path.pardir, 'nosexunit'))

# Add the plugin folder in the path
sys.path.append(plugfld)