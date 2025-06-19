'''
Job. It is composed of several operations.

@author: Vassilissa Lehoux
'''
from typing import List, Optional

from src.scheduling.instance.operation import Operation


class Job(object):
    '''
    Job class.
    Contains information on the next operation to schedule for that job
    '''

    def __init__(self, job_id: int, operations: Optional[List[Operation]] = None):
        '''
        Constructor
        
        Args:
            job_id (int): Identifiant unique du job
            operations (List[Operation], optional): Liste des opérations du job
        '''
        self._job_id = job_id
        self._operations: List[Operation] = operations if operations is not None else []
        self._next_operation_index = 0 
        
        # Assurer l'ordre des opérations et les contraintes de précédence
        if self._operations:
            self._setup_precedence_constraints()
        
    @property
    def job_id(self) -> int:
        '''
        Returns the id of the job.
        '''
        return self._job_id

    def reset(self):
        '''
        Resets the planned operations
        '''
        self._next_operation_index = 0
        # Reset également l'état de planification de chaque opération
        for operation in self._operations:
            operation.reset_scheduling()

    @property
    def operations(self) -> List[Operation]:
        '''
        Returns a list of operations for the job
        '''
        return self._operations.copy()  

    @property
    def next_operation(self) -> Optional[Operation]:
        '''
        Returns the next operation to be scheduled
        '''
        if self._next_operation_index < len(self._operations):
            return self._operations[self._next_operation_index]
        return None  

    def schedule_operation(self):
        '''
        Updates the next_operation to schedule
        '''
        if self._next_operation_index < len(self._operations):
            current_operation = self._operations[self._next_operation_index]
            current_operation.mark_as_scheduled()
            self._next_operation_index += 1

    @property
    def planned(self) -> bool:
        '''
        Returns true if all operations are planned
        '''
        return self._next_operation_index >= len(self._operations)

    @property
    def operation_nb(self) -> int:
        '''
        Returns the nb of operations of the job
        '''
        return len(self._operations)

    def add_operation(self, operation: Operation):
        '''
        Adds an operation to the job at the end of the operation list,
        adds the precedence constraints between job operations.
        
        Args:
            operation (Operation): L'opération à ajouter
        '''
    
        if hasattr(operation, 'job_id') and operation.job_id != self._job_id:
            raise ValueError(f"Operation job_id ({operation.job_id}) doesn't match Job job_id ({self._job_id})")
        
        self._operations.append(operation)
        self._setup_precedence_constraints()

    @property
    def completion_time(self) -> float:
        '''
        Returns the job's completion time
        '''
        if not self._operations:
            return 0.0
        
        last_operation = self._operations[-1]
        
        if hasattr(last_operation, 'end_time') and last_operation.end_time is not None:
            return last_operation.end_time
        
        return 0.0
    
    def _setup_precedence_constraints(self):
        '''
        Configure les contraintes de précédence entre les opérations du job.
        Chaque opération doit être terminée avant que la suivante puisse commencer.
        '''
        for i in range(len(self._operations) - 1):
            current_op = self._operations[i]
            next_op = self._operations[i + 1]
            
            if hasattr(current_op, 'add_successor') and hasattr(next_op, 'add_predecessor'):
                current_op.add_successor(next_op)
                next_op.add_predecessor(current_op)
    
    def get_operation_by_index(self, index: int) -> Optional[Operation]:
        '''
        Retourne l'opération à l'index spécifié.
        
        Args:
            index (int): Index de l'opération (0-based)
            
        Returns:
            Operation: L'opération à l'index donné, ou None si l'index est invalide
        '''
        if 0 <= index < len(self._operations):
            return self._operations[index]
        return None
    
    def get_operation_position(self, operation: Operation) -> int:
        '''
        Retourne la position de l'opération dans le job.
        
        Args:
            operation (Operation): L'opération recherchée
            
        Returns:
            int: Position de l'opération (0-based), ou -1 si non trouvée
        '''
        try:
            return self._operations.index(operation)
        except ValueError:
            return -1
    
    def is_operation_ready(self, operation: Operation) -> bool:
        '''
        Vérifie si une opération peut être planifiée (toutes ses prédécesseures sont terminées).
        
        Args:
            operation (Operation): L'opération à vérifier
            
        Returns:
            bool: True si l'opération peut être planifiée, False sinon
        '''
        operation_index = self.get_operation_position(operation)
        if operation_index == -1:
            return False
        
        if operation_index == 0:
            return True
        
        for i in range(operation_index):
            prev_operation = self._operations[i]
            if not (hasattr(prev_operation, 'is_scheduled') and prev_operation.is_scheduled()):
                return False
        
        return True
    
    def get_earliest_start_time(self, operation: Operation) -> float:
        '''
        Calcule le temps de début au plus tôt pour une opération donnée.
        
        Args:
            operation (Operation): L'opération pour laquelle calculer le temps de début
            
        Returns:
            float: Temps de début au plus tôt
        '''
        operation_index = self.get_operation_position(operation)
        if operation_index == -1:
            return 0.0
        
        if operation_index == 0:
            return 0.0
        
        prev_operation = self._operations[operation_index - 1]
        if hasattr(prev_operation, 'end_time') and prev_operation.end_time is not None:
            return prev_operation.end_time
        
        return 0.0
    
    def __str__(self) -> str:
        '''
        Représentation en chaîne du job.
        '''
        status = "completed" if self.planned else f"next: op {self._next_operation_index}"
        return f"Job {self._job_id} ({self.operation_nb} operations, {status})"
    
    def __repr__(self) -> str:
        '''
        Représentation détaillée du job.
        '''
        return f"Job(job_id={self._job_id}, operations={len(self._operations)}, next_index={self._next_operation_index})"
    
    def get_total_processing_time(self, machine_assignments: Optional[dict] = None) -> float:
        '''
        Calcule le temps de traitement total du job sur les machines assignées.
        
        Args:
            machine_assignments (dict, optional): Dictionnaire {operation_id: machine_id}
            
        Returns:
            float: Temps de traitement total
        '''
        total_time = 0.0
        
        for operation in self._operations:
            if machine_assignments and hasattr(operation, 'operation_id'):
                machine_id = machine_assignments.get(operation.operation_id)
                if machine_id is not None and hasattr(operation, 'get_duration_for_machine'):
                    duration = operation.get_duration_for_machine(machine_id)
                    if duration is not None:
                        total_time += duration
            elif hasattr(operation, 'min_duration'):
                total_time += operation.min_duration()
        
        return total_time