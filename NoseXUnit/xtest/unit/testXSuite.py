#-*- coding: utf-8 -*-
import os

import xtest.unit

import plugin

class TestXSuite(xtest.XTestCase):

    def getSuite(self):
        suite = plugin.XSuite('my_module')
        elmt1 = xtest.get_mock_test_case('my_module', 'my_class', 'my_test1')
        test1 = plugin.XTest(plugin.SUCCESS, elmt1)
        suite.addTest(test1)
        elmt2 = xtest.get_mock_test_case('my_module', 'my_class', 'my_test2')
        test2 = plugin.XTest(plugin.SUCCESS, elmt2)
        suite.addTest(test2)
        elmt3 = xtest.get_mock_test_case('my_module', 'my_class', 'my_test3')
        test3 = plugin.XTest(plugin.FAIL, elmt3, xtest.get_err(StandardError, "StandardError raised"))
        suite.addTest(test3)
        elmt4 = xtest.get_mock_test_case('my_module', 'my_class', 'my_test4')
        test4 = plugin.XTest(plugin.ERROR, elmt4, xtest.get_err(StandardError, "StandardError2 raised"))
        suite.addTest(test4)  
        return suite

    def testGetName(self):
        suite = plugin.XSuite('my_module')
        self.assertEquals('my_module', suite.getName())

    def testGetXmlPath(self):
        suite = plugin.XSuite('my_module')
        self.assertEquals('target%sTEST-my_module.2.xml' % os.sep, suite.getXmlPath('target', 'my_module.2'))
        
    def testAddTest(self):
        suite = plugin.XSuite('my_module')
        elmt = xtest.get_mock_test_case('my_module', 'my_class', 'my_test')
        test = plugin.XTest(plugin.SUCCESS, elmt)
        suite.addTest(test)
        self.assertEquals(1, len(suite.tests))
        self.assertEquals(1, suite.count[plugin.SUCCESS])

    def testGetNbrTests(self):
        self.assertEquals(4, self.getSuite().getNbrTests())

    def testGetNbrTestsFromKind(self):
        self.assertEquals(2, self.getSuite().getNbrTestsFromKind(plugin.SUCCESS))

    def testGetNbrTestsFromKindZero(self):
        self.assertEquals(0, self.getSuite().getNbrTestsFromKind(plugin.SKIP))

    def testGetNbrTestsFromKinds(self):
        self.assertEquals(3, self.getSuite().getNbrTestsFromKinds([plugin.SUCCESS, plugin.ERROR, ]))

    def testSetStdout(self):
        suite = plugin.XSuite('my_module')
        suite.setStdout('hello')
        self.assertEquals('hello', suite.stdout) 

    def testSetStderr(self):
        suite = plugin.XSuite('my_module')
        suite.setStderr('hello')
        self.assertEquals('hello', suite.stderr)

    def testWriteXmlOnStreamNoTests(self):
        suite = plugin.XSuite('my_module')
        self.assertWriteOnStreamEquals("""<?xml version="1.0" encoding="UTF-8"?><testsuite name="my_module" tests="0" errors="0" failures="0" time="0.000"><system-out><![CDATA[]]></system-out><system-err><![CDATA[]]></system-err></testsuite>""", suite)      

    def testWriteXmlOnStreamTests(self):
        suite = self.getSuite()
        suite.setStdout('stdout')
        suite.setStderr('stderr')
        expect = ["""<?xml version="1.0" encoding="UTF-8"?><testsuite name="my_module" tests="4" errors="1" failures="1" time="0.000"><testcase classname="my_module.my_class" name="my_test1" time="0.000"/><testcase classname="my_module.my_class" name="my_test2" time="0.000"/><testcase classname="my_module.my_class" name="my_test3" time="0.000"><failure type="exceptions.StandardError"><![CDATA[Traceback (most recent call last)""",
                  """StandardError raised]]></failure></testcase><testcase classname="my_module.my_class" name="my_test4" time="0.000"><error type="exceptions.StandardError"><![CDATA[Traceback (most recent call last)""",
                  """StandardError2 raised]]></error></testcase><system-out><![CDATA[stdout]]></system-out><system-err><![CDATA[stderr]]></system-err></testsuite>""", ]
        self.assertWriteOnStreamContains(expect, suite)  

if __name__=="__main__":
    xtest.main()
