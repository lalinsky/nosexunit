#-*- coding: utf-8 -*-
import os
import sys
import new
import unittest
import StringIO
import nose.suite
import ConfigParser

class XTestCase(unittest.TestCase):
    '''Test class for the project'''

    _pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def setUp(self):
        '''Get the properties from the property file'''
        unittest.TestCase.setUp(self)
        self._properties = {}
        self._pfile = None
        if os.path.exists(os.path.join(self._pdir, 'test.properties.model')):
            self._pfile = os.path.join(self._pdir, 'test.properties.model')
            if os.path.exists(os.path.join(self._pdir, 'test.properties')):
                self._pfile = os.path.join(self._pdir, 'test.properties')
            if self._pfile:
                parser = ConfigParser.ConfigParser()
                parser.read(self._pfile)
                for section in parser.sections():
                    self._properties[section] = {}
                    for option in parser.options(section):
                        self._properties[section][option] = parser.get(section, option)

    def getProperty(self, section, option):
        '''Get the value of the given property'''
        assert self._properties.has_key(section), "No such section in your test.properties(.model) file: %s" % section
        assert self._properties[section].has_key(option), "No such option in section %s in your test.properties(.model) file: %s" % option
        return self._properties[section][option]

    def getUnitProperty(self, option):
        '''Get the value of the property in the unit section'''
        return self.getProperty('unit', option)

    def getIntProperty(self, option):
        '''Get the value of the property in the integration section'''
        return self.getProperty('int', option)

    def assertWriteXmlEquals(self, expected, rpath):
        '''Assert that the given file contain the expected string'''
        rfile = open(rpath, 'r')
        content = rfile.read()
        rfile.close()
        self.assertEquals(expected, content)

    def assertWriteOnStreamEquals(self, expected, cls):
        '''Assert that the method writeXmlOnStream of cls write the given output'''
        stream = StringIO.StringIO()
        try: cls.writeXmlOnStream(stream, cls.getName())
        except: cls.writeXmlOnStream(stream)
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
        try: cls.writeXmlOnStream(stream, cls.getName())
        except: cls.writeXmlOnStream(stream)
        output = stream.getvalue()
        stream.close()
        offset = -1
        for expect in expected:
            res = output.find(expect, offset+1)
            if res == -1 or res <= offset: raise self.failureException, "Xml doesn't match"
            offset = res

class MockTestCase(unittest.TestCase):
    '''Mock the test case class'''
    
    def __init__(self, module, cls, meth):
        '''Init the mock'''
        self.module = module
        self.__module__ = self.module
        self.cls = cls
        self.meth = meth
        
    def id(self):
        '''Return the id of the test'''
        return "%s.%s.%s" % (self.module, self.cls, self.meth)

class Options:
    '''Mock options'''

    def __init__(self, where):
        self.where = where

class Conf:
    '''Configuration file'''
    
    def __init__(self, where):
        '''Init the where clause'''
        self.where = ()
        self.options = Options(where)

class Plugin:
    '''Class of mock for the Plugin module'''

    def help(self):
        pass

    def options(self, parser, env=os.environ):
        pass
        
    def configure(self, options, config):
        pass

    def begin(self):
        pass

    def startTest(self, test):
        pass

    def addError(self, test, err, capt):
        pass

    def addFailure(self, test, err, capt, tb_info):
        pass

    def addSuccess(self, test, capt):
        pass

    def finalize(self, result):
        pass


def get_mock_test_case(module, cls_name, meth):
    '''Retun a mock test case'''
    return new.classobj(cls_name, (MockTestCase,), {})(module, cls_name, meth)
        
def get_err(cls, msg):
    '''Return the sys.exc_info of the given exception'''
    try:
        raise cls(msg)
    except Exception, e:
        return sys.exc_info()

def main():
    unittest.main()
