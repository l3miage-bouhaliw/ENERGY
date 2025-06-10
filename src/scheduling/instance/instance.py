'''
Information for the instance of the optimization problem.

@author: Vassilissa Lehoux
'''
from typing import List
import os
import csv

from src.scheduling.instance.job import Job
from src.scheduling.instance.operation import Operation
from src.scheduling.instance.machine import Machine


class Instance(object):
    '''
    classdocs
    '''

    def __init__(self, instance_name):
        '''
        Constructor
        '''
        raise "Not implemented error"

    @classmethod
    def from_file(cls, folderpath):
        inst = cls(os.path.basename(folderpath))
        # Reading the operation info
        with open(folderpath + os.path.sep + inst._instance_name + '_op.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
            for row in csv_reader:
                # To complete
                pass

        # reading machine info
        with open(folderpath + os.path.sep + inst._instance_name + '_mach.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
            for row in csv_reader:
                # To complete
                pass
        # To complete
        raise "Not implemented error"
        return inst

    @property
    def name(self):
        raise "Not implemented error"

    @property
    def machines(self) -> List[Machine]:
        raise "Not implemented error"

    @property
    def jobs(self) -> List[Job]:
        raise "Not implemented error"

    @property
    def operations(self) -> List[Operation]:
        raise "Not implemented error"

    @property
    def nb_jobs(self):
        raise "Not implemented error"

    @property
    def nb_machines(self):
        raise "Not implemented error"

    @property
    def nb_operations(self):
        raise "Not implemented error"

    def __str__(self):
        return f"{self.name}_M{self.nb_machines}_J{self.nb_jobs}_O{self.nb_operations}"

    def get_machine(self, machine_id) -> Machine:
        raise "Not implemented error"

    def get_job(self, job_id) -> Job:
        raise "Not implemented error"

    def get_operation(self, operation_id) -> Operation:
        raise "Not implemented error"
