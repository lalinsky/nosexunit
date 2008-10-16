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
        module = test_NoseXUnit.Module('foo', content)
        module.save(self.source)
        content = """
import foo
self.assertEquals('hello', foo.hello())
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
