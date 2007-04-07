#-*- coding: utf-8 -*-
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'nosexunit'))

import xtest
import plugin

class TestXTestElmt(xtest.XTestCase):
    
    def testInitTestElmt(self):
        elmt = plugin.XTestElmt('elmt')
        self.assertEquals('elmt', elmt.elmt)
        self.assertEquals(None, elmt.begin)
        self.assertEquals(None, elmt.end)
        
    def testSetStart(self):
        elmt = plugin.XTestElmt('elmt')
        elmt.setStart(10)
        self.assertEquals(10, elmt.begin)
        
    def testSetEnd(self):
        elmt = plugin.XTestElmt('elmt')
        elmt.setStop(20)
        self.assertEquals(20, elmt.end)

    def testGetTime(self):
        elmt = plugin.XTestElmt('elmt')
        elmt.setStart(5)
        elmt.setStop(20)
        self.assertEquals(15, elmt.getTime())
        
    def testGetDefaultTimeNoBeginNoEnd(self):
        elmt = plugin.XTestElmt('elmt')
        self.assertEquals(plugin.UNK_TIME, elmt.getTime())

    def testGetDefaultTimeNoBegin(self):
        elmt = plugin.XTestElmt('elmt')
        elmt.end = 10
        self.assertEquals(plugin.UNK_TIME, elmt.getTime())

    def testGetDefaultTimeNoEnd(self):
        elmt = plugin.XTestElmt('elmt')
        elmt.begin = 10
        self.assertEquals(plugin.UNK_TIME, elmt.getTime())

    def testStart(self):
        elmt = plugin.XTestElmt('elmt')
        elmt.start()
        self.assertTrue(elmt.begin > 0)
        
    def testStop(self):
        elmt = plugin.XTestElmt('elmt')
        elmt.stop()
        self.assertTrue(elmt.end > 0)

    def testDelta(self):
        elmt = plugin.XTestElmt('elmt')
        elmt.start()
        time.sleep(1)
        elmt.stop()
        self.assertTrue(elmt.getTime() > 0)

    def testEqualsBetweenXTestElmt(self):
        desc = 'elmt'
        elmt1 = plugin.XTestElmt(desc)
        elmt2 = plugin.XTestElmt(desc)
        self.assertTrue(elmt1.equals(elmt2))

    def testNotEqualsBetweenXTestElmt(self):
        elmt1 = plugin.XTestElmt('elmt1')
        elmt2 = plugin.XTestElmt('elmt2')
        self.assertFalse(elmt1.equals(elmt2))

    def testEqualsBetweenXTestElmtAndTest(self):
        desc = 'elmt'
        elmt = plugin.XTestElmt(desc)
        self.assertTrue(elmt.equals(desc))

    def testNotEqualsBetweenXTestElmtAndTest(self):
        desc = 'elmt1'
        elmt = plugin.XTestElmt('elmt2')
        self.assertFalse(elmt.equals(desc))

if __name__=="__main__":
    xtest.main()
