#-*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'nosexunit'))

import xtest
import plugin

class TestStdRecord(xtest.XTestCase):
    
    def testStdOutRecordOn(self):
        recorder = plugin.StdOutRecoder()
        recorder.start()
        sys.stdout.write('hello')
        recorder.stop()
        recorder.end()
        self.assertEquals("hello", recorder.content())
        
    def testStdOutRecordOff(self):
        recorder = plugin.StdOutRecoder()
        sys.stdout.write('hello1')
        recorder.start()
        sys.stdout.write('hello2')
        recorder.stop()
        sys.stdout.write('hello3')
        recorder.end()
        self.assertEquals("hello2", recorder.content())    

    def testStdOutRecordReset(self):
        recorder = plugin.StdOutRecoder()
        recorder.start()
        sys.stdout.write('hello')
        recorder.reset()
        sys.stdout.write('hello3')
        recorder.end()
        self.assertEquals("hello3", recorder.content())   

    def testStdErrRecordOn(self):
        recorder = plugin.StdErrRecorder()
        recorder.start()
        sys.stderr.write('hello')
        recorder.stop()
        recorder.end()
        self.assertEquals("hello", recorder.content())
        
    def testStdErrRecordOff(self):
        recorder = plugin.StdErrRecorder()
        sys.stderr.write('hello1')
        recorder.start()
        sys.stderr.write('hello2')
        recorder.stop()
        sys.stderr.write('hello3')
        recorder.end()
        self.assertEquals("hello2", recorder.content())    

    def testStdErrRecordReset(self):
        recorder = plugin.StdErrRecorder()
        recorder.start()
        sys.stderr.write('hello')
        recorder.reset()
        sys.stderr.write('hello3')
        recorder.end()
        self.assertEquals("hello3", recorder.content())   

        
if __name__=="__main__":
    xtest.main()