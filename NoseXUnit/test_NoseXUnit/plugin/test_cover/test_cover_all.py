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
def tutu():
    return "tutu"
    
    
"""
        module = test_NoseXUnit.Module('foo_1', content)
        module.save(self.source)
        content = """
def tata():
    return "tata"

def toto(): return 'foo' #pragma: no cover
    
    
"""
        module = test_NoseXUnit.Module('foo_2', content)
        module.save(self.source)
        content = """
import foo_1
self.assertEquals('hello', foo_1.hello())
"""
        test = test_NoseXUnit.TestModule('test_foo', 'TestFoo')
        test.addCustom('test', content)
        test.save(self.source)
        self.suitepath = self.source
        self.setUpCore(self.core_target, self.source)
        self.setUpCover(self.cover_target, False)
        print self.args
        print self.cover_target
        print self.target

    def test(self):
        print self.output

if __name__=="__main__":
    test_NoseXUnit.main()
