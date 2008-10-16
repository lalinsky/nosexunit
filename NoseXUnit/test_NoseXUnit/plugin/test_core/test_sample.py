#-*- coding: utf-8 -*-
import os
import test_NoseXUnit

import nosexunit.tools as ntools
import nosexunit.excepts as nexcepts

class TestClean(test_NoseXUnit.PluginTestCase):
    
    def setUpCase(self):
        test = test_NoseXUnit.TestModule('test_Gp3Tester', 'TestGp3Tester')
        test.addSuccess('testOK')
        test.addError('testKO')
        test.addFailure('testKO2')
        test.addSkip('testSkip')
        test.addDeprecated('testDep')
        test.save(self.source)
        self.suitepath = self.source
        self.setUpCore(self.core_target, self.source)

    def test(self):
        print self.output

if __name__=="__main__":
    test_NoseXUnit.main()
