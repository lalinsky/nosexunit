#-*- coding: utf-8 -*-
import os
import test_NoseXUnit

import nosexunit.tools as ntools
import nosexunit.excepts as nexcepts

class TestClean(test_NoseXUnit.PluginTestCase):
    
    # Detect \x0c <-> '' which means a new page
    
    def setUpCase(self):
        content = """
a
b
"""
        test_NoseXUnit.Module('foo_1', content).save(self.source)
        test_NoseXUnit.Module('foo_2', content).save(self.source)
        test_NoseXUnit.Module('foo_3', content).save(self.source)
        test_NoseXUnit.Module('foo_4', content).save(self.source)
        self.suitepath = self.source
        self.setUpCore(self.core_target, self.source)
        self.setUpAudit(self.audit_target)

    def test(self):
        print self.output

if __name__=="__main__":
    test_NoseXUnit.main()
