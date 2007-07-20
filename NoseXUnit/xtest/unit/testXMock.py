#-*- coding: utf-8 -*-
import xtest.unit

class TestXMock(xtest.XTestCase):

    def testTestCaseTestId(self):
        test = xtest.get_mock_case('my_module', 'my_class', 'my_method')
        self.assertEquals('my_module.my_class.my_method', test.id())


if __name__=="__main__":
    xtest.main()
