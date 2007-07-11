#-*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import nose.suite

# If test mode, import the Plugin from xtest, else import the real one
# --------------------------------------------------------------------
if __name__ == os.path.basename(__file__).split('.')[0]:
    from xtest import Plugin
    sys.stderr.write("WARNING: Mock mode for NoseXUnit")
else:
    from nose.plugins.base import Plugin

# Test result possibilities
# -------------------------
# Test success
SUCCESS = 0
# Test failure
FAIL = 1
# Test error
ERROR = 2
# Test Skipped
SKIP = 3
# Test deprecated
DEPRECATED = 4

# Value for unknown execution time
# --------------------------------
UNK_TIME = 0

# Test output prefix
# ------------------
XML_PREFIX = "TEST-"

# The folders to excludes
# -----------------------
EX_SEARCH = ['.svn', '.cvs', ]


class XUnitException(StandardError):
    '''Exception for NoseXUnit process'''
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

    def __init__(self):
        '''Init the test element'''
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


class XSuite(XTestElmt):
    '''Class for the suite notion'''

    def __init__(self, module):
        '''Init the suite'''
        XTestElmt.__init__(self)
        self.module = module
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
        return self.module

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

    def getXmlName(self, folder):
        '''
        Return the name of the suite for the XML
        Avoid data erasing
        '''
        name = self.getName()
        path = self.getXmlPath(folder, name)
        if not os.path.exists(path): return name
        else:
            cpt = 1
            while True:
                name = "%s.%d" % (self.getName(), cpt)
                path = self.getXmlPath(folder, name)
                if not os.path.exists(path): return name
                cpt += 1

    def getXmlPath(self, folder, xml_name):
        '''Return the output xml path'''
        return os.path.join(folder, '%s%s.xml' % (XML_PREFIX, xml_name))

    def writeXml(self, folder):
        '''Write the xml file on disk'''
        if self.getNbrTestsFromKinds([SUCCESS, FAIL, ERROR, ]) > 0:
            xname = self.getXmlName(folder)
            xpath = self.getXmlPath(folder, xname)
            xfile = open(xpath, 'w')
            self.writeXmlOnStream(xfile, xname)
            xfile.close()

    def writeXmlOnStream(self, stream, xname):
        '''Write the test suite on the stream'''
        nbrTests = self.getNbrTestsFromKinds([SUCCESS, ERROR, FAIL, ])
        nbrFails = self.getNbrTestsFromKind(FAIL)
        nbrErrors = self.getNbrTestsFromKind(ERROR)
        stream.write('<?xml version="1.0" encoding="UTF-8"?>')
        stream.write('<testsuite name="%s" tests="%d" errors="%d" failures="%d" time="%.3f">' % (xname, nbrTests, nbrErrors, nbrFails, self.getTime()))
        for test in self.tests:
            test.writeXmlOnStream(stream)
        stream.write('<system-out><![CDATA[%s]]></system-out>' % self.stdout)
        stream.write('<system-err><![CDATA[%s]]></system-err>' % self.stderr)
        stream.write('</testsuite>')
    

class XTest(XTestElmt):
    '''Class for the test notion'''

    def __init__(self, kind, elmt, err=None, capt=None, tb_info=None):
        '''Init the test result'''
        XTestElmt.__init__(self)
        self.elmt = elmt
        self.kind = kind
        self.err = err
        self.capt = capt
        self.tb_info = tb_info

    def getKind(self):
        '''Return the kind of text'''
        return self.kind

    def getName(self):
        '''Return the name of the method'''
        return self.elmt.id().split('.')[-1]

    def getClass(self):
        '''Return the class name'''
        return "%s.%s" % (self.elmt.__module__, self.elmt.__class__.__name__)

    def _get_err_type(self):
        '''Return the human readable error type for err'''
        if self.err != None:
            return '%s.%s' % (self.err[1].__class__.__module__, self.err[1].__class__.__name__)
        else: return None

    def _get_err_formated(self):
        '''Return the the formated error for output'''
        if self.err != None:
            return '<![CDATA[%s]]>' % '\n'.join((''.join(traceback.format_exception(*self.err))).split('\n')[:-1])
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


class NoseXUnit(Plugin, object):

    def help(self):
        '''Help'''
        return "Output XML report of test status"

    def options(self, parser, env=os.environ):
        '''Add lauch options for nosexunit'''
        Plugin.options(self, parser, env)
        parser.add_option("--xml-report-folder", action="store", default="target/xml-report", dest="report", help="Folder to output XML report to (default is target/xml-report).")
        parser.add_option("--source-folder", action="store", default=None, dest="src", help="Set the python's source folder, and add it in the path (optional).")
        parser.add_option("--recursive", action="store_true", default=False, dest="recursive", help="Walk in the source folder to add deeper folders in the path if they don't contain __init__.py file. Works only if --source-folder is defined.")
        parser.add_option("--want-folder", action="store_true", default=False, dest="wantfld", help="Search tests in folders with no __init__.py file (default does nothing).")
        
    def configure(self, options, config):
        '''Configure the plugin'''
        Plugin.configure(self, options, config)
        self.conf = config
        self.repfld = os.path.abspath(options.report)
        if options.src != None: self.src = os.path.abspath(options.src)
        else: self.src = None
        self.recursive = options.recursive
        self.wantfld = options.wantfld
        
    def initialize(self):
        '''Set the environment'''
        # If a source folder is specified, check the existance
        if self.src != None and not os.path.isdir(self.src):
            raise XUnitException("the source folder doesn't exists: %s" % self.src)
        # Create the report folder if doesn't exists, else clean it
        if not os.path.isdir(self.repfld):
            if os.path.isfile(self.repfld):
                raise XUnitException("the report folder exists but is not a folder: %s" % self.repfld)
            else: os.makedirs(self.repfld)
        else:
            for elmt in os.listdir(self.repfld):
                if elmt.startswith(XML_PREFIX): os.remove(os.path.join(self.repfld, elmt))
        # Add the source folder and eventually all his tree in the sys.path
        if self.src != None:
            sys.path.append(self.src)
            if self.recursive:
                for dirpath, dirnames, filenames in os.walk(self.src):
                    for elmt in EX_SEARCH:
                        if elmt in dirnames: dirnames.remove(elmt)
                    if not os.path.exists(os.path.join(dirpath, '__init__.py')):
                        sys.path.append(dirpath)

    def begin(self):
        '''Initialize the plugin'''
        self.initialize()
        self.module = None
        self.suite = None
        self.start = None
        self.stdout = StdOutRecoder()
        self.stderr = StdErrRecorder()

    def wantDirectory(self, dirname):
        '''Define the wanted directory'''
        if self.wantfld and not os.path.exists(os.path.join(dirname, '__init__.py')):
            return True
        else: return

    def enableSuite(self, test):
        '''Check that suite exists. If not exists, create a new one'''
        if self.module != test.__module__:
            self.module = test.__module__
            self.stopSuite()
            self.startSuite(self.module)

    def startSuite(self, module):
        '''Start a new suite'''
        self.suite = XSuite(module)
        self.suite.start()
        self.stderr.reset()
        self.stdout.reset()
        self.stderr.start()
        self.stdout.start()
   
    def startTest(self, test):
        '''Record starting time'''
        self.enableSuite(test)
        self.start = time.time()

    def addTestCase(self, kind, test, err=None, capt=None, tb_info=None):
        '''Add a new test result in the current suite'''
        elmt = XTest(kind, test, err=err, capt=capt, tb_info=tb_info)
        elmt.setStart(self.start)
        elmt.stop()
        self.enableSuite(test)
        self.suite.addTest(elmt)

    def addError(self, test, err, capt):
        '''Add a error test'''
        kind = ERROR
        if isinstance(test, nose.SkipTest): kind = SKIP
        elif isinstance(test, nose.DeprecatedTest): kind = DEPRECATED
        self.addTestCase(kind, test, err=err, capt=capt)

    def addFailure(self, test, err, capt, tb_info):
        '''Add a failure test'''
        self.addTestCase(FAIL, test, err=err, capt=capt, tb_info=tb_info)

    def addSuccess(self, test, capt):
        '''Add a successful test'''
        self.addTestCase(SUCCESS, test, capt=capt)

    def stopSuite(self):
        '''Stop the current suite'''
        if self.suite != None:
            self.stdout.stop()
            self.stderr.stop()
            self.suite.stop()
            self.suite.setStdout(self.stdout.content())
            self.suite.setStderr(self.stderr.content())
            self.suite.writeXml(self.repfld)
            self.suite = None

    def finalize(self, result):
        '''Set the old standard outputs'''
        self.stopSuite()
        self.stderr.end()
        self.stdout.end()

 
