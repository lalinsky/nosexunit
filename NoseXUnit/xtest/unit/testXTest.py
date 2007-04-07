#-*- coding: utf-8 -*-
import xtest.unit

import plugin

class TestXTest(xtest.XTestCase):
    
    def testGetKind(self):
        test = plugin.XTest(plugin.ERROR, None)
        self.assertEquals(plugin.ERROR, test.getKind())

if __name__=="__main__":
    xtest.main()
