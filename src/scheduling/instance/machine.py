'''
Machine on which operation are executed.

@author: Vassilissa Lehoux
'''
from typing import List
from src.scheduling.instance.operation import Operation


class Machine(object):
    '''
    Machine class.
    When operations are scheduled on the machine, contains the relative information. 
    '''

    def __init__(self, machine_id: int, set_up_time: int, set_up_energy: int, tear_down_time: int,
                 tear_down_energy:int, min_consumption: int, end_time: int):
        '''
        Constructor
        Machine is stopped at the beginning of the planning and need to
        be started before executing any operation.
        @param end_time: End of the schedule on this machine: the machine must be
          shut down before that time.
        '''
        raise "Not implemented error"

    def reset(self):
        raise "Not implemented error"

    @property
    def set_up_time(self) -> int:
        raise "Not implemented error"

    @property
    def tear_down_time(self) -> int:
        raise "Not implemented error"

    @property
    def machine_id(self) -> int:
        raise "Not implemented error"

    @property
    def scheduled_operations(self) -> List:
        '''
        Returns the list of the scheduled operations on the machine.
        '''
        raise "Not implemented error"

    @property
    def available_time(self) -> int:
        """
        Returns the next time at which the machine is available
        after processing its last operation of after its last set up.
        """
        raise "Not implemented error"

    def add_operation(self, operation: Operation, start_time: int) -> int:
        '''
        Adds an operation on the machine, at the end of the schedule,
        as soon as possible after time start_time.
        Returns the actual start time.
        '''
        raise "Not implemented error"
  
    def stop(self, at_time):
        """
        Stops the machine at time at_time.
        """
        assert(self.available_time >= at_time)
        raise "Not implemented error"

    @property
    def working_time(self) -> int:
        '''
        Total time during which the machine is running
        '''
        raise "Not implemented error"

    @property
    def start_times(self) -> List[int]:
        """
        Returns the list of the times at which the machine is started
        in increasing order
        """
        raise "Not implemented error"

    @property
    def stop_times(self) -> List[int]:
        """
        Returns the list of the times at which the machine is stopped
        in increasing order
        """
        raise "Not implemented error"

    @property
    def total_energy_consumption(self) -> int:
        """
        Total energy consumption of the machine during planning exectution.
        """
        raise "Not implemented error"

    def __str__(self):
        return f"M{self.machine_id}"

    def __repr__(self):
        return str(self)
