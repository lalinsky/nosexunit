#-*- coding: utf-8 -*-
import os
import sys
import test_NoseXUnit

import nosexunit.audit as naudit
import nosexunit.tools as ntools
import nosexunit.excepts as nexcepts

class TestAudit(test_NoseXUnit.TestCase):
    pass
#    def test(self):
#        source = test_NoseXUnit.Module('olivier')
#        source.save(self.work)
#        sys.path.append(self.work)
##        naudit.audit([source.desc(), ], 'text', self.work)
        
        
if __name__=="__main__":
    test_NoseXUnit.main()