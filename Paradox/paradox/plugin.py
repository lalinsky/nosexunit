#-*- coding: utf-8 -*-
import nose
import logging
import traceback
import nose.plugins

# Get a logger
logger =  logging.getLogger('nose.%s' % __name__)

class Paradox(nose.plugins.Plugin, object):
    '''Plugin that tests NoseXUnit'''

    def help(self):
        '''Help'''
        return 'How to get NoseXUnit reports without NoseXUnit? That is the question!'

    def begin(self):
        '''Store test results'''
        # Store success
        self.success = []
        # Store errors
        self.errors = []
        # Store failures
        self.failures = []

    def addError(self, test, err):
        '''Add an error'''
        if not isinstance(test, nose.SkipTest) and not isinstance(test, nose.DeprecatedTest): self.errors.append( (test, err) )

    def addFailure(self, test, err):
        '''Add a failure'''
        self.failures.append( (test, err) )

    def addSuccess(self, test):
        '''Add a success'''
        self.success.append(test)

    def finalize(self, result):
        '''Create the report'''
        # Get the tests total
        total = len(self.success) + len(self.errors) + len(self.failures)
        # Get the output for each test
        tests = []
        # Add success
        tests.extend( ["<testcase classname='%s' name='%s' time='0' />" % (klass(test), method(test)) for test in self.success ] )
        # Add failures
        tests.extend( ["<testcase classname='%s' name='%s' time='0'><failure type='%s'>%s</failure></testcase>" % (klass(test), method(test), error(err), trace(err)) for test, err in self.failures ] )
        # Add errors
        tests.extend( ["<testcase classname='%s' name='%s' time='0'><error type='%s'>%s</error></testcase>" % (klass(test), method(test), error(err), trace(err)) for test, err in self.errors ] )
        # Get the output
        content = """<?xml version="1.0" encoding="UTF-8"?>
<testsuite name='NoseXUnit' tests='%d' errors='%d' failures='%d' time='0'>
%s
<system-out/>
<system-err/>
</testsuite>
""" % (total, len(self.errors), len(self.failures), '\n'.join(tests))
        # Get the file
        fd = open('NoseXUnit.xml', 'w')
        # Set the content
        fd.write(content)
        # Close the file
        fd.close()

def klass(test):
    '''Get the class of a test'''
    return '.'.join(test.id().split('.')[:-1])

def method(test):
    '''Get the function'''
    return test.id().split('.')[-1]

def error(err):
    '''Get the error description'''
    return '%s.%s' % (err[1].__class__.__module__, err[1].__class__.__name__)

def trace(err):
    '''Get the trace of the error'''
    return '<![CDATA[%s]]>' % '\n'.join((''.join(traceback.format_exception(*err))).split('\n')[:-1])
