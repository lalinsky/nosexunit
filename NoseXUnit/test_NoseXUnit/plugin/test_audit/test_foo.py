#-*- coding: utf-8 -*-
import os
import test_NoseXUnit

import nosexunit.tools as ntools
import nosexunit.excepts as nexcepts

class TestClean(test_NoseXUnit.PluginTestCase):
    
    def setUpCase(self):
        content = """
def hello():
    return "hello"
"""
        package = test_NoseXUnit.Package('foo_1')
        package.append(test_NoseXUnit.Module('foo_2', content))
        package.save(self.source)
        self.suitepath = self.source
        self.setUpCore(self.core_target, self.source)
        self.setUpAudit(self.audit_target)
        print self.target

    def test(self):
        print self.output

if __name__=="__main__":
    test_NoseXUnit.main()
