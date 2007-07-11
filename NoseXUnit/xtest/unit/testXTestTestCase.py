#-*- coding: utf-8 -*-
import xtest.unit

import plugin

class TestXTestTestCase(xtest.XTestCase):
        
    def testGetName(self):
        case = xtest.get_mock_test_case('my_module', 'my_class', 'my_method')
        test = plugin.XTest(plugin.ERROR, case)
        self.assertEquals('my_method', test.getName())

    def testGetClass(self):
        case = xtest.get_mock_test_case('my_module', 'my_class', 'my_method')
        test = plugin.XTest(plugin.ERROR, case)
        self.assertEquals('my_module.my_class', test.getClass())
         
    def testWriteOnXmlSuccess(self):
        case = xtest.get_mock_test_case('my_module', 'my_class', 'my_method')
        test = plugin.XTest(plugin.SUCCESS, case)
        self.assertWriteOnStreamEquals("""<testcase classname="my_module.my_class" name="my_method" time="0.000"/>""", test)

    def testWriteOnXmlError(self):
        case = xtest.get_mock_test_case('my_module', 'my_class', 'my_method')
        err = xtest.get_err(StandardError, 'StrandadError raised')
        test = plugin.XTest(plugin.ERROR, case, err=err)
        self.assertWriteOnStreamContains(["""<testcase classname="my_module.my_class" name="my_method" time="0.000"><error type="exceptions.StandardError"><![CDATA[Traceback (most recent call last)""", """]]></error></testcase>""", ], test)

    def testWriteOnXmlFailure(self):
        case = xtest.get_mock_test_case('my_module', 'my_class', 'my_method')
        err = xtest.get_err(StandardError, 'StrandadError raised')
        test = plugin.XTest(plugin.FAIL, case, err=err)
        self.assertWriteOnStreamContains(["""<testcase classname="my_module.my_class" name="my_method" time="0.000"><failure type="exceptions.StandardError"><![CDATA[Traceback (most recent call last)""", """]]></failure></testcase>""", ], test)
        
    def testWriteOnXmlSkip(self):
        case = xtest.get_mock_test_case('my_module', 'my_class', 'my_method')
        test = plugin.XTest(plugin.SKIP, case)
        self.assertWriteOnStreamEquals('', test)

    def testWriteOnXmlDeprecated(self):
        case = xtest.get_mock_test_case('my_module', 'my_class', 'my_method')
        test = plugin.XTest(plugin.DEPRECATED, case)
        self.assertWriteOnStreamEquals('', test)

if __name__=="__main__":
    xtest.main()
