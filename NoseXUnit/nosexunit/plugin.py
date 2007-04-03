#-*- coding: utf-8 -*-
import os
import sys
import time
import unittest
import traceback
import nose.suite

# If test mode, import the Plugin from xtest, else import the real one
try:
    from xtest import Plugin
    print "WARNING: Mock mode for Plugin"
except:
    from nose.plugins.base import Plugin

# Test result possibilities
SUCCESS = 0
FAIL = 1
ERROR = 2
SKIP = 3
DEPRECATED = 4

# Values fr non-specified fields
UNK_DESC = "unknown"
UNK_TIME = 0

# Test output prefix
XML_PREFIX = "TEST-"

# The folders to excludes
EX_SEARCH = ['.svn', ]

class XUnitException(StandardError):
    pass

class StdRecorder:
    '''Class to capture the standard outputs'''
    
    def __init__(self):
        '''Initialize with an empty record'''
        self.rec = False
        self.record = ''

    def __getattr__(self, attr):
        '''Call the functions on the output'''
        return getattr(self.save, attr)
    
    def write(self, string):
        '''Write on the record and on the standard output'''
        if self.rec: self.record += string
        return self.save.write(string)
    
    def start(self):
        '''Start to record the stream given by constructor'''
        self.rec = True
        
    def stop(self):
        '''Stop recording the steam given by constructor'''
        self.rec = False

    def content(self):
        '''Return the content of the record'''
        return self.record

    def reset(self):
        '''Reset the recorder'''
        self.record = ''
    
    def end(self):
        '''End the recorder'''
        self.stop()


class StdOutRecoder(StdRecorder):
    '''Class to record the standard output'''
    
    def __init__(self):
        '''Replace the sys.stdout output by this one'''
        StdRecorder.__init__(self)
        self.save = sys.stdout
        sys.stdout = self
        
    def end(self):
        '''Replace the sys.stdout output by his old value'''
        StdRecorder.end(self)
        sys.stdout = self.save

class StdErrRecorder(StdRecorder):
    '''Class to record the error output'''
    
    def __init__(self):
        '''Replace the sys.stderr output by this one'''
        StdRecorder.__init__(self)
        self.save = sys.stderr
        sys.stderr = self
        
    def end(self):
        '''Replace the sys.stderr output by his old value'''
        StdRecorder.end(self)
        sys.stderr = self.save


class XTestElmt:
    '''Root class for suites and tests'''

    def __init__(self, elmt):
        '''Init the test element'''
        self.elmt = elmt
        self.begin = None
        self.end = None

    def start(self):
        '''Set the start time'''
        self.begin = time.time()

    def stop(self):
        '''Set the end time'''
        self.end = time.time()

    def setStart(self, begin):
        '''Set the start time'''
        self.begin = begin
        
    def setStop(self, end):
        '''Set the end time'''
        self.end = end    

    def getTime(self):
        '''Get the running time'''
        if self.begin != None and self.end != None:
            return self.end - self.begin
        else: return UNK_TIME

    def __eq__(self, elmt):
        '''
        Equality fonction for the test elements.
        Be carefull to the operators
        The first element of the test must of the type XTestElmt if the second one is TestCase or TestModule'''
        if isinstance(elmt, XTestElmt):
            return self.elmt == elmt.elmt
        else:
            try: return self.elmt == elmt
            except: return False
            
    def equals(self, elmt):
        '''Same as equals, but remove the __eq__ ambiguity'''
        return self == elmt


class XSuite(XTestElmt):
    '''Class for the suite notion'''

    def __init__(self, elmt):
        '''Init the suite'''
        XTestElmt.__init__(self, elmt)
        self.tests = []
        self.count = {}
        self.stdout = ''
        self.stderr = ''

    def setStderr(self, string):
        '''Set the standard outputs for the suite'''
        self.stderr = string
        
    def setStdout(self, string):
        '''Set the error outputs for the suite'''
        self.stdout = string

    def getName(self):
        '''Get the name of the suite'''
        return self.elmt.moduleName

    def addTest(self, test):
        '''Add a test in the right section'''
        self.tests.append(test)
        kind = test.getKind()
        if self.count.has_key(kind): self.count[kind] += 1
        else: self.count[kind] = 1

    def getNbrTests(self):
        '''Return the total number of test'''
        nbrTests = 0
        for kind in self.count.keys():
            nbrTests += self.count[kind]
        return nbrTests

    def getNbrTestsFromKind(self, kind):
        '''Get the number of tests given the kind'''
        if self.count.has_key(kind):
            return self.count[kind]
        else: return 0

    def getNbrTestsFromKinds(self, kinds):
        '''Get the number of tests given the kind'''
        nbrTests = 0
        for kind in kinds:
            nbrTests += self.getNbrTestsFromKind(kind)
        return nbrTests

    def getXmlPath(self, folder):
        '''Return the output xml path'''
        return os.path.join(folder, '%s%s.xml' % (XML_PREFIX, self.getName()))

    def writeXml(self, folder):
        '''Write the xml file on disk'''
        if self.getNbrTestsFromKinds([SUCCESS, FAIL, ERROR, ]) > 0:
            xpath = self.getXmlPath(folder)
            xfile = open(xpath, 'w')
            self.writeXmlOnStream(xfile)
            xfile.close()

    def writeXmlOnStream(self, stream):
        '''Write the test suite on the stream'''
        nbrTests = self.getNbrTestsFromKinds([SUCCESS, ERROR, FAIL, ])
        nbrFails = self.getNbrTestsFromKind(FAIL)
        nbrErrors = self.getNbrTestsFromKind(ERROR)
        stream.write('<?xml version="1.0" encoding="UTF-8"?>')
        stream.write('<testsuite name="%s" tests="%d" errors="%d" failures="%d" time="%.3f">' % (self.getName(), nbrTests, nbrErrors, nbrFails, self.getTime()))
        for test in self.tests:
            test.writeXmlOnStream(stream)
        stream.write('<system-out><![CDATA[%s]]></system-out>' % self.stdout)
        stream.write('<system-err><![CDATA[%s]]></system-err>' % self.stderr)
        stream.write('</testsuite>')
    

class XTest(XTestElmt):
    '''Class for the test notion'''

    def __init__(self, kind, elmt, err=None, capt=None, tb_info=None):
        XTestElmt.__init__(self, elmt)
        self.kind = kind
        self.err = err
        self.capt = capt
        self.tb_info = tb_info

    def getKind(self):
        '''Return the kind of text'''
        return self.kind

    def getName(self):
        '''Return the name of the method'''
        if isinstance(self.elmt, unittest.TestCase):
            return self.elmt.id().split('.')[-1]
        elif isinstance(self.elmt, nose.suite.TestModule):
            return self.elmt.moduleName
        else: return UNK_DESC

    def getClass(self):
        '''Return the class name'''
        if isinstance(self.elmt, unittest.TestCase):
            return '.'.join(self.elmt.id().split('.')[:-1])
        elif isinstance(self.elmt, nose.suite.TestModule):
            return self.elmt.moduleName
        else: return UNK_DESC

    def _get_err_type(self):
        '''Return the human readable error type for err'''
        if self.err != None:
            return '%s.%s' % (self.err[1].__class__.__module__, self.err[1].__class__.__name__)
        else: return None

    def _get_err_formated(self):
        '''Return the the formated error for output'''
        if self.err != None:
            return '\n'.join((''.join(traceback.format_exception(*self.err))).split('\n')[:-1])
            #formated = ''
            #for line in traceback.format_exception(*self.err):
            #    for l in line.split('\n')[:-1]: formated += l
            #return formated
        else: return None

    def writeXmlOnStream(self, stream):
        '''Write the xml result on the stream'''
        if self.kind in [SUCCESS, FAIL, ERROR, ]:
            stream.write('<testcase classname="%s' % self.getClass() + '" name="%s' % self.getName() + '"' + ' time="%.3f"' % self.getTime())
            if self.kind == SUCCESS: stream.write('/>')
            else:
                stream.write('>')
                if self.kind == ERROR: tag = 'error'
                else: tag = 'failure'
                stream.write('<%s type="%s">' % (tag, self._get_err_type()))
                stream.write(self._get_err_formated())
                stream.write('</%s>' % tag)
                stream.write('</testcase>')


#class XInitSuite(XSuite):
#    '''Suite which check that there are __init__.py in the tests folder'''
#    
#    def __init__(self):
#        '''Init the init suite'''
#        XSuite.__init__(self, None)
#    
#    def getName(self):
#        '''Get the name of the suite'''
#        return 'NoseXUnitInitSuite'
#
#class XInitTest(XTest):
#    '''Test taht check that there are __init__.py in the test folder'''
#    
#    def getName(self):
#        '''Get the name of the test case'''
#        name = 'FindInitIn'
#        for fld in self.elmt.split(os.sep):
#            if fld != '': name += fld.capitalize().replace(':', 'TwoPoints').replace('.', 'Point').replace('_', 'Underscore')
#        return name
#    
#    def getClass(self):
#        '''Get the class of the test'''
#        return 'NoseXUnitPlugin'
    

class NoseXUnit(Plugin, object):

    def help(self):
        return "Output XML report of test status"

    def add_options(self, parser, env=os.environ):
        Plugin.add_options(self, parser, env)
        parser.add_option("--xml-report-folder", action="store", default="target/xml-report", dest="report", help="Folder to output XML report to")
        parser.add_option("--source-folder", action="store", default="python/src", dest="src", help="Set the python's source folder, and add it in the path")
        parser.add_option("--recursive", action="store_true", default=False, dest="recursive", help="Walk in the source folder to add deeper folders in the path")
    
    def configure(self, options, config):
        Plugin.configure(self, options, config)
        self.conf = config
        self.repfld = os.path.abspath(options.report)
        self.src = os.path.abspath(options.src)
        self.recursive = options.recursive
        
    def initialize(self):
        '''Set the environment'''
        if not os.path.isdir(self.src):
            raise XUnitException("the source folder doesn't exists: %s" % self.src)
        if not os.path.isdir(self.repfld):
            if os.path.isfile(self.repfld):
                raise XUnitException("the report folder exists but is not a folder: %s" % self.repfld)
            else: os.makedirs(self.repfld)
        else:
            for elmt in os.listdir(self.repfld):
                if elmt.startswith(XML_PREFIX): os.remove(os.path.join(self.repfld, elmt))
        if not self.recursive: sys.path.append(self.src)
        else:
            for dirpath, dirnames, filenames in os.walk(self.src):
                for elmt in EX_SEARCH:
                    if elmt in dirnames: dirnames.remove(elmt)
                sys.path.append(dirpath)

    def begin(self):
        '''Initialize the plugin'''
        self.initialize()
        self.suite = None
        self.start = None
        self.stdout = StdOutRecoder()
        self.stderr = StdErrRecorder()
        #initSuite = XInitSuite()
        #for where in self.conf.where:
        #    for dirpath, dirnames, filenames in os.walk(where):
        #        if '.svn' in dirnames: dirnames.remove('.svn')
        #        for dirname in dirnames:
        #            subdir = os.path.join(dirpath, dirname)
        #            init = os.path.join(subdir, '__init__.py')
        #            if not os.path.isfile(init):
        #                try:
        #                    raise XUnitException("can't find __init__.py in the following folder: %s" % subdir)
        #                except Exception, e:
        #                    err = sys.exc_info()
        #                    initTest = XInitTest(ERROR, subdir, err=err)
        #                    initSuite.addTest(initTest)
        #initSuite.writeXml(self.repfld)            

    def wantDirectory(self, dirname):
        '''Define the wanted directory'''
        if os.path.basename(dirname) in EX_SEARCH: return False
        elif os.path.exists(os.path.join(dirname, '__init__.py')): return False
        else: return True
        
    def startTest(self, test):
        '''Define the operations to perform when starting a test'''
        self.start = time.time()
        if self.isSuiteBegin(test):
            self.suite = XSuite(test)
            self.suite.start()
            self.stderr.reset()
            self.stdout.reset()
            self.stderr.start()
            self.stdout.start()

    def isSuiteBegin(self, test):
        '''Return True if this is a new suite which begins'''
        try: return isinstance(test, nose.suite.TestModule)
        except: return False

    def isSuiteEnd(self, test):
        '''Return True if the current suite is ending'''
        try: return self.suite.equals(test)
        except: return False

    def addTestCase(self, kind, test, err=None, capt=None, tb_info=None):
        '''Add a new test result in the current suite'''
        elmt = XTest(kind, test, err=err, capt=capt, tb_info=tb_info)
        elmt.setStart(self.start)
        elmt.stop()
        self.suite.addTest(elmt)
    
    def addDeprecated(self, test):
        '''Add a deprecated test'''
        self.addTestCase(DEPRECATED, test)

    def addError(self, test, err, capt):
        '''Add a error test'''
        self.addTestCase(ERROR, test, err=err, capt=capt)

    def addFailure(self, test, err, capt, tb_info):
        '''Add a failure test'''
        self.addTestCase(FAIL, test, err=err, capt=capt, tb_info=tb_info)

    def addSkip(self, test):
        '''Add a skipped test'''
        self.addTestCase(SKIP, test)

    def addSuccess(self, test, capt):
        '''Add a successful test'''
        self.addTestCase(SUCCESS, test, capt=capt)

    def stopTest(self, test):
        '''Stop the test'''
        if self.isSuiteEnd(test):
            self.stdout.stop()
            self.stderr.stop()
            self.suite.stop()
            self.suite.setStdout(self.stdout.content())
            self.suite.setStderr(self.stderr.content())
            self.suite.writeXml(self.repfld)
            self.suite = None

    def finalize(self, result):
        '''Set the old standard outputs'''
        self.stderr.end()
        self.stdout.end()

    
