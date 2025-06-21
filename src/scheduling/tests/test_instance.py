import unittest
import tempfile
import shutil
import os
import csv

from src.scheduling.instance.instance import Instance

class TestInstance(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self._create_test_instance_files(self.test_dir)
        self.instance = Instance.from_file(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _create_test_instance_files(self, directory):
        prefix = os.path.basename(directory)
        operations_file = os.path.join(directory, f'{prefix}_op.csv')
        machines_file = os.path.join(directory, f'{prefix}_mach.csv')

        # Create operations file with the format expected by Instance.from_file
        # Format: job_id, operation_id, machine_ids, durations, energies
        with open(operations_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['job_id', 'operation_id', 'machine_ids', 'durations', 'energies'])
            # Operation 1: Job 1, can run on machines 1 or 2
            writer.writerow([1, 1, '1;2', '5.0;6.0', '10.0;12.0'])
            # Operation 2: Job 1, can run on machine 2
            writer.writerow([1, 2, '2', '3.0', '8.0'])
            # Operation 3: Job 2, can run on machines 1 or 2
            writer.writerow([2, 3, '1;2', '4.0;5.0', '9.0;11.0'])

        # Create machines file with the format expected by Instance.from_file
        # Format: machine_id, startup_time, startup_energy, shutdown_time, shutdown_energy, idle_energy_per_time
        with open(machines_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['machine_id', 'startup_time', 'startup_energy', 'shutdown_time', 'shutdown_energy', 'idle_energy_per_time'])
            writer.writerow([1, 1.0, 2.0, 1.0, 2.0, 0.5])
            writer.writerow([2, 1.5, 3.0, 1.5, 3.0, 0.8])

    # Tests

    def test_instance_loaded(self):
        self.assertIsNotNone(self.instance)
        self.assertEqual(self.instance.nb_jobs, 2)
        self.assertEqual(self.instance.nb_machines, 2)
        self.assertEqual(self.instance.nb_operations, 3)

    def test_get_job(self):
        job = self.instance.get_job(1)
        self.assertIsNotNone(job)
        self.assertEqual(job.job_id, 1)
        # Check that job has operations
        self.assertGreater(len(job.operations), 0)

    def test_get_machine(self):
        machine = self.instance.get_machine(2)
        self.assertIsNotNone(machine)
        self.assertEqual(machine.machine_id, 2)

    def test_get_operation(self):
        op = self.instance.get_operation(3)
        self.assertIsNotNone(op)
        self.assertEqual(op.operation_id, 3)
        self.assertEqual(op.job_id, 2)

    def test_get_operations_for_machine(self):
        # Test operations that can run on machine 1
        ops_machine_1 = self.instance.get_operations_for_machine(1)
        self.assertIsInstance(ops_machine_1, list)
        self.assertGreater(len(ops_machine_1), 0)
        
        # Operations 1 and 3 should be able to run on machine 1
        op_ids = [op.operation_id for op in ops_machine_1]
        self.assertIn(1, op_ids)
        self.assertIn(3, op_ids)

        # Test operations that can run on machine 2
        ops_machine_2 = self.instance.get_operations_for_machine(2)
        self.assertIsInstance(ops_machine_2, list)
        self.assertGreater(len(ops_machine_2), 0)
        
        # All operations (1, 2, 3) should be able to run on machine 2
        op_ids = [op.operation_id for op in ops_machine_2]
        self.assertIn(1, op_ids)
        self.assertIn(2, op_ids)
        self.assertIn(3, op_ids)

    def test_validate_instance(self):
        # Test the actual validation method from Instance class
        valid = self.instance.validate_instance()
        self.assertTrue(valid)

    def test_instance_properties(self):
        # Test various properties
        self.assertEqual(len(self.instance.jobs), 2)
        self.assertEqual(len(self.instance.machines), 2)
        self.assertEqual(len(self.instance.operations), 3)
        
        # Test instance name
        self.assertIsNotNone(self.instance.name)

    def test_job_operations_relationship(self):
        # Test that jobs contain their operations correctly
        job1 = self.instance.get_job(1)
        job1_operation_ids = [op.operation_id for op in job1.operations]
        self.assertIn(1, job1_operation_ids)
        self.assertIn(2, job1_operation_ids)
        
        job2 = self.instance.get_job(2)
        job2_operation_ids = [op.operation_id for op in job2.operations]
        self.assertIn(3, job2_operation_ids)

    def test_operation_machine_compatibility(self):
        # Test that operations know which machines they can run on
        op1 = self.instance.get_operation(1)
        self.assertTrue(hasattr(op1, 'available_machines'))
        self.assertIn(1, op1.available_machines)
        self.assertIn(2, op1.available_machines)
        
        op2 = self.instance.get_operation(2)
        self.assertIn(2, op2.available_machines)
        self.assertEqual(len(op2.available_machines), 1)  # Only machine 2

    def test_nonexistent_ids_raise_errors(self):
        # Test that requesting non-existent IDs raises KeyError
        with self.assertRaises(KeyError):
            self.instance.get_job(999)
        
        with self.assertRaises(KeyError):
            self.instance.get_machine(999)
        
        with self.assertRaises(KeyError):
            self.instance.get_operation(999)


if __name__ == '__main__':
    unittest.main()