#-*- coding: utf-8 -*-
import os
import test_NoseXUnit

import nosexunit.audit as naudit
import nosexunit.tools as ntools
import nosexunit.excepts as nexcepts

#class TestDoPages(test_NoseXUnit.TestCase):
#    
#    def test_ok(self):
#        naudit.do_pages(['foo_1', 'foo_2', ], self.target)
#        i_found = ntools.load(os.path.join(self.target, 'index.html'))
#        c_found = ntools.load(os.path.join(self.target, 'content.html'))
#        c_s_found = ntools.load(os.path.join(self.target, 'content_single.html'))
#        i_expected = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
#<html>
#  <head>
#    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
#    <title>NoseXUNit - Audit</title>
#  </head>
#  <frameset cols="22%,*">
#    <frame name="left_panel" src="content.html" scrolling="yes" />
#    <frame name="right_panel" src="foo_1/pylint_global.html" scrolling="yes" />
#    <noframes>
#      <body>
#        This document is designed to be viewed using the frames feature. If you see this message, you are using a non-frame-capable web client.
#        <br/>
#        Link to <a href="content_single.html">Non-frame version.</a>
#      </body>
#    </noframes>
#  </frameset>
#</html>
#"""
#        self.assertEquals(i_expected, i_found)
#        c_expected = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
#<html>
#  <head>
#    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
#    <title>NoseXUnit - Audit Content</title>
#  </head>
#  <body>
#    <h1>NoseXUnit<h1>
#    <table>
#      <tr><td><a href="foo_1/pylint_global.html" target="right_panel">foo_1</a></td></tr>
#<tr><td><a href="foo_2/pylint_global.html" target="right_panel">foo_2</a></td></tr>
#    </table>
#  </body>
#</html>
#"""
#        self.assertEquals(c_expected, c_found)
#        c_s_expected = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
#<html>
#  <head>
#    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
#    <title>NoseXUnit - Audit Content</title>
#  </head>
#  <body>
#    <h1>NoseXUnit<h1>
#    <table>
#      <tr><td><a href="foo_1/pylint_global.html" >foo_1</a></td></tr>
#<tr><td><a href="foo_2/pylint_global.html" >foo_2</a></td></tr>
#    </table>
#  </body>
#</html>
#"""
#        self.assertEquals(c_s_expected, c_s_found)
#        
#    def test_ko(self):
#        self.assertRaises(nexcepts.AuditError, naudit.do_pages, [], self.target)

if __name__=="__main__":
    test_NoseXUnit.main()