#!/usr/bin/env python3

from tests import unittests
import unittest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittests.suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
