#-*- coding: utf-8 -*-
import os
import sys
import unittest
import StringIO
import nose.suite
import ConfigParser

class XTestCase(unittest.TestCase):
    '''Test class for the project'''

    _dir = None

    def setUp(self):
        '''Get the properties from the property file'''
        unittest.TestCase.setUp(self)
        self._properties = {}
        if self._dir != None:
            pfile = None
            if os.path.exists(os.path.join(self._dir, 'test.properties.model')):
                pfile = os.path.join(self._dir, 'test.properties.model')
                if os.path.exists(os.path.join(self._dir, 'test.properties')):
                    pfile = os.path.join(self._dir, 'test.properties')
                if pfile:
                    parser = ConfigParser.ConfigParser()
                    parser.read(pfile)
                    for section in parser.sections():
                        for option in parser.options(section):
                            self._properties[option] = parser.get(section, option)

    def getProperty(self, property):
        '''Get the value of the given property'''
        assert self._properties.has_key(property), "No such property in your test.properties file: %s" % property
        return self._properties[property]

    def assertWriteXmlEquals(self, expected, rpath):
        '''Assert that the given file contain the expected string'''
        rfile = open(rpath, 'r')
        content = rfile.read()
        rfile.close()
        self.assertEquals(expected, content)

    def assertWriteOnStreamEquals(self, expected, cls):
        '''Assert that the method writeXmlOnStream of cls write the given output'''
        stream = StringIO.StringIO()
        cls.writeXmlOnStream(stream)
        output = stream.getvalue()
        stream.close()
        self.assertEquals(expected, output)
 
    def assertWriteXmlContains(self, expected, rpath):
        '''Assert that the given file contain the expected strings'''
        rfile = open(rpath, 'r')
        content = rfile.read()
        rfile.close()
        offset = -1
        for expect in expected:
            res = content.find(expect, offset+1)
            if res == -1 or res <= offset: raise self.failureException, "Xml doesn't match"
            offset = res
 
    def assertWriteOnStreamContains(self, expected, cls):
        '''Assert that the method writeXmlOnStream of cls write the given output'''
        stream = StringIO.StringIO()
        cls.writeXmlOnStream(stream)
        output = stream.getvalue()
        stream.close()
        offset = -1
        for expect in expected:
            res = output.find(expect, offset+1)
            if res == -1 or res <= offset: raise self.failureException, "Xml doesn't match"
            offset = res

class MockTestModule(nose.suite.TestModule):
    '''Mock the test suite class'''
    
    def __init__(self, moduleName):
        '''Init the mock'''
        self.moduleName = moduleName
    
    def __eq__(self, obj):
        '''Equal function for the test suite'''
        try:
            return self.moduleName == obj.moduleName
        except:
            return False
    
class MockTestCase(unittest.TestCase):
    '''Mock the test case class'''
    
    def __init__(self, testId):
        '''Init the mock'''
        self.testId = testId
    
    def id(self):
        '''Return the id of the test'''
        return self.testId
    
    def __eq__(self, obj):
        '''Equal function for the test case'''
        try:
            return self.id() == obj.id()
        except:
            return False
        
def get_err(cls, msg):
    '''Return the sys.exc_info of the given exception'''
    try:
        raise cls(msg)
    except Exception, e:
        return sys.exc_info()


class Conf:
    '''Configuration file'''
    
    def __init__(self, where):
        '''Init the where clause'''
        self.where = where
        

class Plugin:
    '''Class of mock for the Plugin module'''

    def add_options(self, parser, env=os.environ):
        pass

    def configure(self, options, config):
        pass

    def addDeprecated(self, test):
        pass

    def addError(self, test, err, capt):
        pass

    def addFailure(self, test, err, capt, tb_info):
        pass

    def addSkip(self, test):
        pass        

    def addSuccess(self, test, capt):
        pass        
            
    def begin(self):
        pass

    def finalize(self, result):
        pass
    
    #def loadTestsFromModule(self, module):
    
    #def loadTestsFromName(self, name, module=None, importPath=None):

    #def loadTestsFromPath(self, path, module=None, importPath=None):
    
    #def loadTestsFromTestCase(self, cls):
    
    #def prepareTest(self, test):
    
    #def report(self, stream):

    #def setOutputStream(self, stream):

    def startTest(self, test):
        pass
    
    def stopTest(self, test):
        pass

    def wantClass(self, cls):
        pass
    
    def wantDirectory(self, dirname):
        pass
    
    def wantFile(self, file, package=None):
        pass
    
    def wantFunction(self, function):
        pass
    
    def wantMethod(self, method):
        pass
    
    def wantModule(self, module):
        pass
    
    def wantModuleTests(self, module):
        pass


def main():
    unittest.main()