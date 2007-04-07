#-*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'nosexunit'))

import xtest
import plugin

class TestXTestTestCase(xtest.XTestCase):
        
    def testGetName(self):
        case = xtest.MockTestCase('my_module.my_class.my_method')
        test = plugin.XTest(plugin.ERROR, case)
        self.assertEquals('my_method', test.getName())

    def testGetClass(self):
        case = xtest.MockTestCase('my_module.my_class.my_method')
        test = plugin.XTest(plugin.ERROR, case)
        self.assertEquals('my_module.my_class', test.getClass())
         
    def testWriteOnXmlSuccess(self):
        case = xtest.MockTestCase('my_module.my_class.my_method')
        test = plugin.XTest(plugin.SUCCESS, case)
        self.assertWriteOnStreamEquals("""<testcase classname="my_module.my_class" name="my_method" time="0.000"/>""", test)

    def testWriteOnXmlError(self):
        case = xtest.MockTestCase('my_module.my_class.my_method')
        err = xtest.get_err(StandardError, 'StrandadError raised')
        test = plugin.XTest(plugin.ERROR, case, err=err)
        self.assertWriteOnStreamContains(["""<testcase classname="my_module.my_class" name="my_method" time="0.000"><error type="exceptions.StandardError">Traceback (most recent call last)""", """</error></testcase>""", ], test)

    def testWriteOnXmlFailure(self):
        case = xtest.MockTestCase('my_module.my_class.my_method')
        err = xtest.get_err(StandardError, 'StrandadError raised')
        test = plugin.XTest(plugin.FAIL, case, err=err)
        self.assertWriteOnStreamContains(["""<testcase classname="my_module.my_class" name="my_method" time="0.000"><failure type="exceptions.StandardError">Traceback (most recent call last)""", """</failure></testcase>""", ], test)
        
    def testWriteOnXmlSkip(self):
        case = xtest.MockTestCase('my_module.my_class.my_method')
        test = plugin.XTest(plugin.SKIP, case)
        self.assertWriteOnStreamEquals('', test)

    def testWriteOnXmlDeprecated(self):
        case = xtest.MockTestCase('my_module.my_class.my_method')
        test = plugin.XTest(plugin.DEPRECATED, case)
        self.assertWriteOnStreamEquals('', test)

    def testEqualsBetweenXTest(self):
        case = xtest.MockTestCase('my_module.my_class.my_method')
        test1 = plugin.XTest(plugin.SUCCESS, case)
        test2 = plugin.XTest(plugin.SUCCESS, case)
        self.assertTrue(test1.equals(test2))

    def testEqualsBetweenXTestAndTestCase(self):
        case = xtest.MockTestCase('my_module.my_class.my_method')
        test = plugin.XTest(plugin.SUCCESS, case)
        self.assertTrue(test.equals(test))

    def testNotEqualsBetweenXTest(self):
        case1 = xtest.MockTestCase('my_module.my_class.my_method')
        case2 = xtest.MockTestCase('my_module2.my_class2.my_method2')
        test1 = plugin.XTest(plugin.SUCCESS, case1)
        test2 = plugin.XTest(plugin.SUCCESS, case2)
        self.assertFalse(test1.equals(test2))

    def testNotEqualsBetweenXTestAndTestCase(self):
        case1 = xtest.MockTestCase('my_module.my_class.my_method')
        case2 = xtest.MockTestCase('my_module2.my_class2.my_method2')
        test = plugin.XTest(plugin.SUCCESS, case2)
        self.assertFalse(test.equals(case1))

if __name__=="__main__":
    xtest.main()
