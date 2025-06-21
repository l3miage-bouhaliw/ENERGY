import unittest
from src.scheduling.instance.machine import Machine
from src.scheduling.instance.operation import Operation


class TestMachine(unittest.TestCase):

    def setUp(self):
        self.machine = Machine(
            machine_id=1,
            set_up_time=5,
            set_up_energy=10,
            tear_down_time=3,
            tear_down_energy=5,
            min_consumption=2,
            end_time=100
        )

        # Création d'une opération valide
        self.op1 = Operation(job_id=1, operation_id=1)
        self.op1.get_duration_for_machine = lambda machine_id: 10 if machine_id == 1 else None
        self.op1.get_energy_for_machine = lambda machine_id: 20 if machine_id == 1 else None
        self.op1.can_be_executed_on_machine = lambda machine_id: machine_id == 1

        self.op2 = Operation(job_id=1, operation_id=2)
        self.op2.get_duration_for_machine = lambda machine_id: 15 if machine_id == 1 else None
        self.op2.get_energy_for_machine = lambda machine_id: 30 if machine_id == 1 else None
        self.op2.can_be_executed_on_machine = lambda machine_id: machine_id == 1

    def test_add_operation_and_energy_consumption(self):
        start_time1 = self.machine.add_operation(self.op1, 0)
        self.assertEqual(start_time1, 5)  # 0 + set_up_time

        start_time2 = self.machine.add_operation(self.op2, start_time1 + 10)
        self.assertEqual(start_time2, 15)  # Direct après op1

        # Vérifier les opérations planifiées
        self.assertEqual(len(self.machine.scheduled_operations), 2)

        # Vérifier l’énergie : set_up + op1 + op2 + pas encore de stop
        expected_energy = 10 + 20 + 30 + self.machine._calculate_idle_time() * 2
        self.assertEqual(self.machine.total_energy_consumption, expected_energy)

    def test_stop_machine(self):
        self.machine.add_operation(self.op1, 0)
        self.machine.stop(self.machine.available_time)
        self.assertFalse(self.machine._is_running)
        self.assertEqual(len(self.machine.stop_times), 1)

    def test_force_shutdown_at_end(self):
        self.machine.add_operation(self.op1, 0)
        self.machine.force_shutdown_at_end()
        self.assertFalse(self.machine._is_running)
        self.assertTrue(len(self.machine.stop_times) >= 1)

    def test_validate_schedule(self):
        self.machine.add_operation(self.op1, 0)
        self.machine.add_operation(self.op2, self.machine.available_time)
        self.machine.force_shutdown_at_end()
        self.assertTrue(self.machine.validate_schedule())

    def test_cannot_execute_on_machine(self):
        bad_op = Operation(job_id=1, operation_id=99)
        bad_op.get_duration_for_machine = lambda machine_id: None
        bad_op.get_energy_for_machine = lambda machine_id: None
        bad_op.can_be_executed_on_machine = lambda machine_id: False
        with self.assertRaises(ValueError):
            self.machine.add_operation(bad_op, 0)

    def test_shutdown_too_late(self):
        machine = Machine(
            machine_id=2,
            set_up_time=1,
            set_up_energy=1,
            tear_down_time=10,
            tear_down_energy=1,
            min_consumption=1,
            end_time=20
        )
        op = Operation(job_id=2, operation_id=1)
        op.get_duration_for_machine = lambda machine_id: 5
        op.get_energy_for_machine = lambda machine_id: 5
        op.can_be_executed_on_machine = lambda machine_id: True
        machine.add_operation(op, 0)
        with self.assertRaises(ValueError):
            machine.stop(15)  # Trop tard pour shutdown proprement


if __name__ == '__main__':
    unittest.main()
