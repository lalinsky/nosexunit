#-*- coding: utf-8 -*-
import os
import sys
import shutil
import optparse

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'nosexunit'))


import xtest
import plugin

class TestNoseXUnit(xtest.XTestCase):

    _dir = os.path.join(os.path.abspath(os.path.dirname(__file__)))

    def setUp(self):
        xtest.XTestCase.setUp(self)
        self.workspace = self.getProperty('workspace')
        self.src = os.path.join(os.path.join(self.workspace, 'python'), 'src')
        self.test = os.path.join(os.path.join(self.workspace, 'python'), 'test')
        self.report = os.path.join(self.workspace, 'report')

    def tearDown(self):
        xtest.XTestCase.tearDown(self)
        if os.path.exists(self.workspace):
            shutil.rmtree(self.workspace)

    def getPlugin(self):
        return plugin.NoseXUnit()

    def getParser(self):
        return optparse.OptionParser()

    def getOptions(self, cls, argv=[]):
        parser = self.getParser()
        cls.add_options(parser)
        return parser.parse_args(argv)[0]
    
    def getConf(self, where):
        return xtest.Conf(where)

    def getPluginWithWorkspace(self, recursive, srcs=[], tsts=[], reports=None):
        if os.path.exists(self.workspace):
            shutil.rmtree(self.workspace)
        plug = self.getPlugin()
        argv = ['--xml-report-folder', self.report, '--source-folder', self.src, ]
        if recursive:
            argv.append('--recursive')
        opts = self.getOptions(plug, argv)
        conf = self.getConf([self.test, ])
        os.makedirs(self.test)
        os.makedirs(self.src)
        def init(folder, elmt):
            abspath = os.path.join(folder, elmt)
            if abspath.endswith('.py') or abspath.endswith('.xml'):
                fld = os.path.dirname(abspath)
                if not os.path.exists(fld):
                    os.makedirs(fld)
                if not os.path.exists(abspath):
                    open(abspath, 'w').close()
            else:
                if not os.path.exists(abspath):
                    os.makedirs(abspath)
        for elmt in srcs:
            init(self.src, elmt)
        for elmt in tsts:
            init(self.test, elmt)
        if reports != None:
            for elmt in reports:
                init(self.report, elmt)
        plug.configure(opts, conf)
        return plug

    def testAddOptionsDefault(self):
        options = self.getOptions(self.getPlugin())
        self.assertEquals(options.report, 'target/xml-report')
        self.assertEquals(options.src, 'python/src')
        self.assertFalse(options.recursive)

    def testAddOptionsReport(self):
        options = self.getOptions(self.getPlugin(), ['--xml-report-folder', 'hello/guy', ])
        self.assertEquals(options.report, 'hello/guy')

    def testAddOptionsSource(self):
        options = self.getOptions(self.getPlugin(), ['--source-folder', 'hello/guy', ])
        self.assertEquals(options.src, 'hello/guy')

    def testAddOptionsRecursive(self):
        options = self.getOptions(self.getPlugin(), ['--recursive', ])
        self.assertTrue(options.recursive)
        
    def testAddAnyFolder(self):
        options = self.getOptions(self.getPlugin(), ['--add-any-folder', ])
        self.assertTrue(options.addAnyFolder)

    def testBeginFailWhenNoSourceFolder(self):
        plug = self.getPluginWithWorkspace(False)
        plug.src = 'folder/which/doesnt/exists'
        self.failUnlessRaises(plugin.XUnitException, plug.begin)     
    
    def testReportFolderCreationIfNotExists(self):
        plug = self.getPluginWithWorkspace(False)
        plug.begin()
        self.assertTrue(os.path.isdir(self.report))
    
    def testReportFolderCleanedIfExists(self):
        plug = self.getPluginWithWorkspace(False, reports=['%smy.test.module.xml' % plugin.XML_PREFIX, ])
        plug.begin()
        self.assertEquals([], os.listdir(self.report))
        
    def testSrcFolderAddedInPath(self):
        plug = self.getPluginWithWorkspace(False, srcs=['my_module.py', 'toto/my_module2.py'])
        plug.begin()
        import my_module
        try:
            import my_module2
            self.failureException, "module should not have been imported"
        except: pass

    def testSrcFolderAddedInPath(self):
        plug = self.getPluginWithWorkspace(False, srcs=['my_module.py', 'toto/my_module2.py'])
        plug.begin()
        import my_module
        try:
            import my_module2
            self.failureException, "module should not have been imported"
        except: pass

    def testSrcFolderAddedInPathRecursive(self):
        plug = self.getPluginWithWorkspace(True, srcs=['my_module.py', 'toto/my_module2.py'])
        plug.begin()
        import my_module
        import my_module2

    def testSrcFolderAddedInPathRecursiveButNotSvn(self):
        plug = self.getPluginWithWorkspace(True, srcs=['my_module.py', 'toto/my_module2.py', '.svn/my_module3.py'])
        import my_module
        import my_module2
        try:
            import my_module3
            self.failureException, "module should not have been imported"
        except: pass
        
    def testNoErrorWhenNoInitLevelOne(self):
        plug = self.getPluginWithWorkspace(False)
        plug.begin()
        self.assertEquals([], os.listdir(self.report))

    def testNoErrorWhenInitLevel2(self):
        plug = self.getPluginWithWorkspace(False, tsts=['toto/__init__.py' ])
        plug.begin()
        self.assertEquals([], os.listdir(self.report))

    #def testErrorWhenNoInitMoreThanOne(self):
    #    plug = self.getPluginWithWorkspace(False, tsts=['toto', 'tata'])
    #    plug.begin()
    #    rpath = os.path.join(self.report, 'TEST-NoseXUnitInitSuite.xml')
    #    self.assertTrue(os.path.isfile(rpath))
    #    expected = ["""<?xml version="1.0" encoding="UTF-8"?><testsuite name="NoseXUnitInitSuite" tests="2" errors="2" failures="0" time="0.000"><testcase classname="NoseXUnitPlugin" name=""",
    #                """time="0.000"><error type="plugin.XUnitException">Traceback (most recent call last)""",
    #                """</error></testcase><testcase classname="NoseXUnitPlugin" name=""",
    #                """time="0.000"><error type="plugin.XUnitException">Traceback (most recent call last)""",
    #                """</error></testcase><system-out><![CDATA[]]></system-out><system-err><![CDATA[]]></system-err></testsuite>""", ]
    #    self.assertWriteXmlContains(expected, rpath)

    def testScenarioOneSuccessSuite(self):
        plug = self.getPluginWithWorkspace(False)
        suite = xtest.MockTestModule('my_module')
        test = xtest.MockTestCase('my_module.my_class.my_method')
        plug.begin()
        plug.startTest(suite)
        plug.startTest(test)
        plug.addSuccess(test, '')
        plug.stopTest(test)
        plug.stopTest(suite)
        plug.finalize(None)
        rpath = os.path.join(self.report, 'TEST-my_module.xml')
        self.assertTrue(os.path.isfile(rpath))
        self.assertWriteXmlEquals("""<?xml version="1.0" encoding="UTF-8"?><testsuite name="my_module" tests="1" errors="0" failures="0" time="0.000"><testcase classname="my_module.my_class" name="my_method" time="0.000"/><system-out><![CDATA[]]></system-out><system-err><![CDATA[]]></system-err></testsuite>""", rpath)


if __name__=="__main__":
    xtest.main()
