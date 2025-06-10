'''
Job. It is composed of several operations.

@author: Vassilissa Lehoux
'''
from typing import List

from src.scheduling.instance.operation import Operation


class Job(object):
    '''
    Job class.
    Contains information on the next operation to schedule for that job
    '''

    def __init__(self, job_id: int):
        '''
        Constructor
        '''
        raise "Not implemented error"
        
    @property
    def job_id(self) -> int:
        '''
        Returns the id of the job.
        '''
        raise "Not implemented error"

    def reset(self):
        '''
        Resets the planned operations
        '''
        raise "Not implemented error"

    @property
    def operations(self) -> List[Operation]:
        '''
        Returns a list of operations for the job
        '''
        raise "Not implemented error"

    @property
    def next_operation(self) -> Operation:
        '''
        Returns the next operation to be scheduled
        '''
        raise "Not implemented error"

    def schedule_operation(self):
        '''
        Updates the next_operation to schedule
        '''
        raise "Not implemented error"

    @property
    def planned(self):
        '''
        Returns true if all operations are planned
        '''
        raise "Not implemented error"

    @property
    def operation_nb(self) -> int:
        '''
        Returns the nb of operations of the job
        '''
        raise "Not implemented error"

    def add_operation(self, operation: Operation):
        '''
        Adds an operation to the job at the end of the operation list,
        adds the precedence constraints between job operations.
        '''
        raise "Not implemented error"

    @property
    def completion_time(self) -> int:
        '''
        Returns the job's completion time
        '''
        raise "Not implemented error"
