'''
Operation of a job.
Its duration and energy consumption depends on the machine on which it is executed.
When operation is scheduled, its schedule information is updated.

@author: Vassilissa Lehoux
'''
from typing import List, Optional


class OperationScheduleInfo:
    '''
    Informations connues quand l'opération est planifiée
    '''

    def __init__(self, machine_id: int, schedule_time: int, duration: int, energy_consumption: int):
        self.machine_id = machine_id
        self.schedule_time = schedule_time
        self.duration = duration
        self.energy_consumption = energy_consumption

    @property
    def end_time(self) -> int:
        return self.schedule_time + self.duration


class Operation:
    '''
    Opération d'un job
    '''

    def __init__(self, job_id: int, operation_id: int):
        self._job_id = job_id
        self._operation_id = operation_id
        self._predecessors: List[Operation] = []
        self._successors: List[Operation] = []
        self._schedule_info: Optional[OperationScheduleInfo] = None

    def __str__(self):
        base_str = f"O{self.operation_id}_J{self.job_id}"
        if self._schedule_info:
            return base_str + f"_M{self.assigned_to}_ci{self.processing_time}_e{self.energy}"
        else:
            return base_str

    def __repr__(self):
        return str(self)

    def reset(self):
        '''
        Supprime les informations de planification
        '''
        self._schedule_info = None

    def add_predecessor(self, operation):
        '''
        Ajoute un prédécesseur à l'opération
        '''
        if operation not in self._predecessors:
            self._predecessors.append(operation)
            operation.add_successor(self)

    def add_successor(self, operation):
        '''
        Ajoute un successeur à l'opération
        '''
        if operation not in self._successors:
            self._successors.append(operation)

    @property
    def operation_id(self) -> int:
        return self._operation_id

    @property
    def job_id(self) -> int:
        return self._job_id

    @property
    def predecessors(self) -> List:
        return self._predecessors

    @property
    def successors(self) -> List:
        return self._successors

    @property
    def assigned(self) -> bool:
        return self._schedule_info is not None

    @property
    def assigned_to(self) -> int:
        if self._schedule_info:
            return self._schedule_info.machine_id
        return -1

    @property
    def processing_time(self) -> int:
        if self._schedule_info:
            return self._schedule_info.duration
        return -1

    @property
    def start_time(self) -> int:
        if self._schedule_info:
            return self._schedule_info.schedule_time
        return -1

    @property
    def end_time(self) -> int:
        if self._schedule_info:
            return self._schedule_info.end_time
        return -1

    @property
    def energy(self) -> int:
        if self._schedule_info:
            return self._schedule_info.energy_consumption
        return -1

    def is_ready(self, at_time: int) -> bool:
        '''
        Retourne True si tous les prédécesseurs sont planifiés et terminés avant at_time
        '''
        for pred in self._predecessors:
            if not pred.assigned or pred.end_time > at_time:
                return False
        return True

    def schedule(self, machine_id: int, at_time: int, duration: int, energy_consumption: int, check_success=True) -> bool:
        '''
        Planifie une opération.
        '''
        if check_success:
            if not self.is_ready(at_time):
                return False

        self._schedule_info = OperationScheduleInfo(machine_id, at_time, duration, energy_consumption)
        return True

    @property
    def min_start_time(self) -> int:
        '''
        Temps minimum de départ selon les contraintes de précédence
        '''
        if not self._predecessors:
            return 0
        return max(pred.end_time for pred in self._predecessors if pred.assigned)

    def schedule_at_min_time(self, machine_id: int, min_time: int, duration: int, energy_consumption: int) -> bool:
        '''
        Essaie de planifier l'opération au min_time ou après selon précédence
        '''
        earliest_time = max(self.min_start_time, min_time)
        return self.schedule(machine_id, earliest_time, duration, energy_consumption, check_success=True)
