import sys
# para Python 2.6 o inferior, utilizamos unittest2
if sys.hexversion < 0x2070000:
    import unittest2 as unittest
else:
    import unittest
    