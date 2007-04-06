#-*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'nosexunit'))

import xtest
import plugin

class TestXInit(xtest.XTestCase):

    def getTest(self):
        return plugin.XInitTest(plugin.ERROR, 'python%stest%snoinit' % (os.sep, os.sep), xtest.get_err(StandardError, "StrandardError raised"))

    def getSuite(self):
        return plugin.XInitSuite()

    def getSuiteWithTest(self):
        suite = self.getSuite()
        suite.addTest(self.getTest())
        return suite

    #def testTestGetName(self):
    #    self.assertEquals('FindInitInPythonTestNoinit', self.getTest().getName())
    #
    #def testTestGetClass(self):
    #    self.assertEquals('NoseXUnitPlugin', self.getTest().getClass())
    #
    #def testSuiteGetName(self):
    #    self.assertEquals('NoseXUnitInitSuite', self.getSuite().getName())
    # 
    #    def testWriteXmlOnStream(self):
    #        suite = self.getSuiteWithTest()
    #        suite.setStdout('stdout')
    #    suite.setStderr('stderr')
    #    expected = ["""<?xml version="1.0" encoding="UTF-8"?><testsuite name="NoseXUnitInitSuite" tests="1" errors="1" failures="0" time="0.000"><testcase classname="NoseXUnitPlugin" name="FindInitInPythonTestNoinit" time="0.000"><error type="exceptions.StandardError">Traceback (most recent call last)""", 
    #                """StrandardError raised</error></testcase><system-out><![CDATA[stdout]]></system-out><system-err><![CDATA[stderr]]></system-err></testsuite>""", ]
    #    self.assertWriteOnStreamContains(expected, suite)  

if __name__=="__main__":
    xtest.main()
