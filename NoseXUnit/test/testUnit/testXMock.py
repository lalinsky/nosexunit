#-*- coding: utf-8 -*-
import os
import sys

import xtest

class TestXMock(xtest.XTestCase):
    
    def testTestModuleModuleName(self):
        moduleName = 'my_module'
        suite = xtest.MockTestModule(moduleName)
        self.assertEquals(moduleName, suite.moduleName)

    def testTestCaseTestId(self):
        testMethodId = 'my_module.my_class.my_method'
        test = xtest.MockTestCase(testMethodId)
        self.assertEquals(testMethodId, test.id())


if __name__=="__main__":
    xtest.main()
