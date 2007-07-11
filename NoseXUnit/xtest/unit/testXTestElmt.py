#-*- coding: utf-8 -*-
import time

import xtest.unit

import plugin

class TestXTestElmt(xtest.XTestCase):
    
    def testInitTestElmt(self):
        elmt = plugin.XTestElmt()
        self.assertEquals(None, elmt.begin)
        self.assertEquals(None, elmt.end)
        
    def testSetStart(self):
        elmt = plugin.XTestElmt()
        elmt.setStart(10)
        self.assertEquals(10, elmt.begin)
        
    def testSetEnd(self):
        elmt = plugin.XTestElmt()
        elmt.setStop(20)
        self.assertEquals(20, elmt.end)

    def testGetTime(self):
        elmt = plugin.XTestElmt()
        elmt.setStart(5)
        elmt.setStop(20)
        self.assertEquals(15, elmt.getTime())
        
    def testGetDefaultTimeNoBeginNoEnd(self):
        elmt = plugin.XTestElmt()
        self.assertEquals(plugin.UNK_TIME, elmt.getTime())

    def testGetDefaultTimeNoBegin(self):
        elmt = plugin.XTestElmt()
        elmt.end = 10
        self.assertEquals(plugin.UNK_TIME, elmt.getTime())

    def testGetDefaultTimeNoEnd(self):
        elmt = plugin.XTestElmt()
        elmt.begin = 10
        self.assertEquals(plugin.UNK_TIME, elmt.getTime())

    def testStart(self):
        elmt = plugin.XTestElmt()
        elmt.start()
        self.assertTrue(elmt.begin > 0)
        
    def testStop(self):
        elmt = plugin.XTestElmt()
        elmt.stop()
        self.assertTrue(elmt.end > 0)

    def testDelta(self):
        elmt = plugin.XTestElmt()
        elmt.start()
        time.sleep(1)
        elmt.stop()
        self.assertTrue(elmt.getTime() > 0)

if __name__=="__main__":
    xtest.main()
