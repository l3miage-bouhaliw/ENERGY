'''
Tests for the Instance class.

@author: Vassilissa Lehoux
'''
import unittest
import os

from src.scheduling.instance.instance import Instance
from src.scheduling.tests.test_utils import TEST_FOLDER_DATA


class TestInstances(unittest.TestCase):


    def setUp(self):
        self.inst = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp1")

    def tearDown(self):
        pass

    def test_from_file(self):
        self.assertEqual(self.inst.name, "jsp1", 'wrong instance name')
        self.assertEqual(self.inst.nb_machines, 4, 'wrong nb of machines')
        self.assertEqual(self.inst.nb_jobs, 2, 'wrong nb of jobs')
        self.assertEqual(self.inst.nb_operations, 4, 'wrong nb of operations')
        self.assertEqual(len(self.inst.machines), 4, 'wrong nb of machines')
        self.assertEqual(len(self.inst.jobs), 2, 'wrong nb of jobs')
        self.assertEqual(str(self.inst), 'jsp1_M4_J2_O4', 'wrong string representation of the instance')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
