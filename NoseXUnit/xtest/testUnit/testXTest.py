#-*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'nosexunit'))

import xtest
import plugin

class TestXTest(xtest.XTestCase):
    
    def testGetKind(self):
        test = plugin.XTest(plugin.ERROR, None)
        self.assertEquals(plugin.ERROR, test.getKind())

if __name__=="__main__":
    xtest.main()
