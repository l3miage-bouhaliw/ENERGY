'''
Machine on which operation are executed.

@author: Vassilissa Lehoux
'''
from typing import List, Tuple, Optional
from src.scheduling.instance.operation import Operation


class ScheduledOperation:
    '''
    Classe auxiliaire pour représenter une opération planifiée sur une machine.
    '''
    def __init__(self, operation: Operation, start_time: int, duration: int, energy: int):
        self.operation = operation
        self.start_time = start_time
        self.duration = duration
        self.energy = energy
        self.end_time = start_time + duration
    
    def __str__(self):
        return f"Op{self.operation.operation_id}[{self.start_time}-{self.end_time}]"


class Machine(object):
    '''
    Machine class.
    When operations are scheduled on the machine, contains the relative information. 
    '''

    def __init__(self, machine_id: int, set_up_time: int, set_up_energy: int, 
                 tear_down_time: int, tear_down_energy: int, min_consumption: int, 
                 end_time: int):
        '''
        Constructor
        Machine is stopped at the beginning of the planning and need to
        be started before executing any operation.
        @param end_time: End of the schedule on this machine: the machine must be
          shut down before that time.
        '''
        self._machine_id = machine_id
        self._set_up_time = set_up_time
        self._set_up_energy = set_up_energy
        self._tear_down_time = tear_down_time
        self._tear_down_energy = tear_down_energy
        self._min_consumption = min_consumption  # Consommation en mode veille
        self._end_time = end_time  # Temps de fin maximum du planning
        
        # État de la machine
        self._scheduled_operations: List[ScheduledOperation] = []
        self._start_times: List[int] = []  # Temps de démarrage
        self._stop_times: List[int] = []   # Temps d'arrêt
        self._is_running = False
        self._current_time = 0  # Temps courant de disponibilité
        
    def reset(self):
        '''
        Remet la machine à son état initial.
        '''
        self._scheduled_operations.clear()
        self._start_times.clear()
        self._stop_times.clear()
        self._is_running = False
        self._current_time = 0

    @property
    def set_up_time(self) -> int:
        '''
        Temps nécessaire pour démarrer la machine.
        '''
        return self._set_up_time

    @property
    def tear_down_time(self) -> int:
        '''
        Temps nécessaire pour arrêter la machine.
        '''
        return self._tear_down_time

    @property
    def machine_id(self) -> int:
        '''
        Identifiant de la machine.
        '''
        return self._machine_id

    @property
    def scheduled_operations(self) -> List[ScheduledOperation]:
        '''
        Returns the list of the scheduled operations on the machine.
        '''
        return self._scheduled_operations.copy()

    @property
    def available_time(self) -> int:
        """
        Returns the next time at which the machine is available
        after processing its last operation or after its last set up.
        """
        return self._current_time

    def add_operation(self, operation: Operation, start_time: int) -> int:
        '''
        Adds an operation on the machine, at the end of the schedule,
        as soon as possible after time start_time.
        Returns the actual start time.
        '''
        # Obtenir la durée et l'énergie pour cette opération sur cette machine
        duration = operation.get_duration_for_machine(self._machine_id)
        energy = operation.get_energy_for_machine(self._machine_id)
        
        if duration is None or energy is None:
            raise ValueError(f"Operation {operation.operation_id} cannot be executed on machine {self._machine_id}")
        
        # Calculer le temps de début effectif
        actual_start_time = max(start_time, self._current_time)
        
        # Si la machine n'est pas en marche, il faut la démarrer
        if not self._is_running:
            # Temps de démarrage nécessaire
            startup_end_time = actual_start_time + self._set_up_time
            self._start_times.append(actual_start_time)
            self._is_running = True
            actual_start_time = startup_end_time
        
        # Vérifier qu'il y a assez de temps pour l'opération et l'arrêt
        operation_end_time = actual_start_time + duration
        if operation_end_time + self._tear_down_time > self._end_time:
            raise ValueError(f"Not enough time to schedule operation {operation.operation_id} and shutdown")
        
        scheduled_op = ScheduledOperation(operation, actual_start_time, duration, energy)
        self._scheduled_operations.append(scheduled_op)
        
        self._current_time = operation_end_time
        
        return actual_start_time

    def stop(self, at_time: int):
        """
        Stops the machine at time at_time.
        """
        if self._current_time > at_time:
            raise ValueError(f"Cannot stop machine at time {at_time}, current time is {self._current_time}")
        
        if self._is_running:
            stop_start_time = max(at_time, self._current_time)
            stop_end_time = stop_start_time + self._tear_down_time
            
            if stop_end_time > self._end_time:
                raise ValueError(f"Cannot shutdown machine before end time {self._end_time}")
            
            self._stop_times.append(stop_start_time)
            self._current_time = stop_end_time
            self._is_running = False

    @property
    def working_time(self) -> int:
        '''
        Total time during which the machine is running
        '''
        total_time = 0
        
        total_time += len(self._start_times) * self._set_up_time
        
        for scheduled_op in self._scheduled_operations:
            total_time += scheduled_op.duration
        
        total_time += len(self._stop_times) * self._tear_down_time
        
        idle_time = self._calculate_idle_time()
        total_time += idle_time
        
        return total_time

    def _calculate_idle_time(self) -> int:
        '''
        Calcule le temps de veille entre les opérations.
        '''
        if not self._scheduled_operations:
            return 0
        
        idle_time = 0
        current_time = 0
        
        for i, start_time in enumerate(self._start_times):
            machine_start = start_time + self._set_up_time
            
            ops_in_period = []
            if i < len(self._stop_times):
                period_end = self._stop_times[i]
                ops_in_period = [op for op in self._scheduled_operations 
                               if machine_start <= op.start_time < period_end]
            else:
                ops_in_period = [op for op in self._scheduled_operations 
                               if op.start_time >= machine_start]
            
            ops_in_period.sort(key=lambda x: x.start_time)
            period_time = machine_start
            
            for op in ops_in_period:
                if op.start_time > period_time:
                    idle_time += op.start_time - period_time
                period_time = op.end_time
        
        return idle_time

    @property
    def start_times(self) -> List[int]:
        """
        Returns the list of the times at which the machine is started
        in increasing order
        """
        return sorted(self._start_times)

    @property
    def stop_times(self) -> List[int]:
        """
        Returns the list of the times at which the machine is stopped
        in increasing order
        """
        return sorted(self._stop_times)

    @property
    def total_energy_consumption(self) -> int:
        """
        Total energy consumption of the machine during planning execution.
        """
        total_energy = 0
        
        # Énergie de démarrage
        total_energy += len(self._start_times) * self._set_up_energy
        
        # Énergie d'arrêt
        total_energy += len(self._stop_times) * self._tear_down_energy
        
        # Énergie des opérations
        for scheduled_op in self._scheduled_operations:
            total_energy += scheduled_op.energy
        
        # Énergie de veille
        idle_time = self._calculate_idle_time()
        total_energy += idle_time * self._min_consumption
        
        return total_energy

    def __str__(self):
        return f"M{self.machine_id}"

    def __repr__(self):
        return f"Machine(id={self.machine_id}, ops={len(self._scheduled_operations)}, running={self._is_running})"
    
    def get_schedule_summary(self) -> str:
        '''
        Retourne un résumé du planning de la machine.
        '''
        if not self._scheduled_operations:
            return f"Machine {self.machine_id}: No operations scheduled"
        
        summary = f"Machine {self.machine_id}:\n"
        
        # Démarrages
        for i, start_time in enumerate(self._start_times):
            summary += f"  Start at {start_time} (duration: {self._set_up_time})\n"
        
        # Opérations
        for op in sorted(self._scheduled_operations, key=lambda x: x.start_time):
            summary += f"  {op}\n"
        
        # Arrêts
        for stop_time in self._stop_times:
            summary += f"  Stop at {stop_time} (duration: {self._tear_down_time})\n"
        
        summary += f"  Total energy: {self.total_energy_consumption}\n"
        summary += f"  Working time: {self.working_time}\n"
        
        return summary
    
    def can_execute_operation(self, operation: Operation) -> bool:
        '''
        Vérifie si cette machine peut exécuter l'opération donnée.
        '''
        return operation.can_be_executed_on_machine(self._machine_id)
    
    def get_operation_cost(self, operation: Operation) -> Tuple[Optional[int], Optional[int]]:
        '''
        Retourne la durée et l'énergie nécessaires pour exécuter une opération.
        
        Returns:
            Tuple[Optional[int], Optional[int]]: (duration, energy) ou (None, None) si impossible
        '''
        if not self.can_execute_operation(operation):
            return None, None
        
        duration = operation.get_duration_for_machine(self._machine_id)
        energy = operation.get_energy_for_machine(self._machine_id)
        
        return duration, energy
    
    def force_shutdown_at_end(self):
        '''
        Force l'arrêt de la machine à la fin du planning si elle est encore en marche.
        '''
        if self._is_running and len(self._stop_times) < len(self._start_times):
            shutdown_start = max(self._current_time, self._end_time - self._tear_down_time)
            if shutdown_start + self._tear_down_time <= self._end_time:
                self.stop(shutdown_start)
            else:
                raise ValueError(f"Cannot shutdown machine {self._machine_id} before end time")
    
    def validate_schedule(self) -> bool:
        '''
        Valide la cohérence du planning de la machine.
        '''
        try:
            for op in self._scheduled_operations:
                if op.start_time < 0 or op.end_time > self._end_time:
                    return False
            
            sorted_ops = sorted(self._scheduled_operations, key=lambda x: x.start_time)
            for i in range(len(sorted_ops) - 1):
                if sorted_ops[i].end_time > sorted_ops[i + 1].start_time:
                    return False
            
            # Vérifier la cohérence des démarrages/arrêts
            if len(self._start_times) < len(self._stop_times):
                return False
            
            return True
            
        except Exception:
            return False