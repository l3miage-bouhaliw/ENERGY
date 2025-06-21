'''
Tests for the Job class

@author: Vassilissa Lehoux
'''
import unittest
from src.scheduling.instance.job import Job
from src.scheduling.instance.operation import Operation

class TestJob(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testCompletionTime(self):
        op1 = Operation(job_id=1, operation_id=1)
        op2 = Operation(job_id=1, operation_id=2)

        # Planifie op1 : start à 0, durée 5 → end = 5
        op1.schedule(machine_id=1, at_time=0, duration=5, energy_consumption=10)

        # Planifie op2 : start à 5, durée 5 → end = 10
        op2.schedule(machine_id=1, at_time=5, duration=5, energy_consumption=10)

        # Création du job avec ces opérations
        job = Job(job_id=1, operations=[op1, op2])

        # Vérification que le completion_time est celui de la dernière opération
        self.assertEqual(job.completion_time, 10)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
