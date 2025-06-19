'''
Information for the instance of the optimization problem.

@author: Vassilissa Lehoux
'''
from typing import List, Dict
import os
import csv

from src.scheduling.instance.job import Job
from src.scheduling.instance.operation import Operation
from src.scheduling.instance.machine import Machine


class Instance(object):
    '''
    Classe représentant une instance du problème d'optimisation de planification.
    Contient les informations sur les jobs, opérations et machines.
    '''

    def __init__(self, instance_name: str):
        '''
        Constructeur de l'instance.
        
        Args:
            instance_name (str): Nom de l'instance
        '''
        self._instance_name = instance_name
        self._machines: List[Machine] = []
        self._jobs: List[Job] = []
        self._operations: List[Operation] = []
        
        # Dictionnaires pour un accès rapide par ID
        self._machines_dict: Dict[int, Machine] = {}
        self._jobs_dict: Dict[int, Job] = {}
        self._operations_dict: Dict[int, Operation] = {}

    @classmethod
    def from_file(cls, folderpath: str):
        """
        Crée une instance à partir des fichiers CSV dans le dossier spécifié.
        
        Args:
            folderpath (str): Chemin vers le dossier contenant les fichiers CSV
            
        Returns:
            Instance: L'instance créée à partir des fichiers
        """
        inst = cls(os.path.basename(folderpath))
        
        # Lecture des informations sur les opérations
        operations_file = os.path.join(folderpath, inst._instance_name + '_op.csv')
        with open(operations_file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  
            
            # Supposons que le header est: job_id, operation_id, machine_ids, durations, energies
            for row in csv_reader:
                if len(row) >= 5:  # Vérification du nombre minimum de colonnes
                    job_id = int(row[0])
                    operation_id = int(row[1])
                    
                    # Parse machine IDs (peut être une liste séparée par des virgules ou points-virgules)
                    machine_ids_str = row[2].strip()
                    if machine_ids_str:
                        machine_ids = [int(x.strip()) for x in machine_ids_str.split(';') if x.strip()]
                    else:
                        machine_ids = []
                    
                    # Parse durations (correspondant aux machine_ids)
                    durations_str = row[3].strip()
                    if durations_str:
                        durations = [float(x.strip()) for x in durations_str.split(';') if x.strip()]
                    else:
                        durations = []
                    
                    # Parse energies (correspondant aux machine_ids)
                    energies_str = row[4].strip()
                    if energies_str:
                        energies = [float(x.strip()) for x in energies_str.split(';') if x.strip()]
                    else:
                        energies = []
                    
                    # Créer l'opération
                    operation = Operation(operation_id, job_id, machine_ids, durations, energies)
                    inst._operations.append(operation)
                    inst._operations_dict[operation_id] = operation

        # Lecture des informations sur les machines
        machines_file = os.path.join(folderpath, inst._instance_name + '_mach.csv')
        with open(machines_file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  
            
            # Supposons que le header est: machine_id, startup_time, startup_energy, shutdown_time, shutdown_energy, idle_energy
            for row in csv_reader:
                if len(row) >= 6: 
                    machine_id = int(row[0])
                    startup_time = float(row[1])
                    startup_energy = float(row[2])
                    shutdown_time = float(row[3])
                    shutdown_energy = float(row[4])
                    idle_energy_per_time = float(row[5])
                    
                    # Créer la machine
                    machine = Machine(machine_id, startup_time, startup_energy, 
                                    shutdown_time, shutdown_energy, idle_energy_per_time)
                    inst._machines.append(machine)
                    inst._machines_dict[machine_id] = machine

        # Création des jobs à partir des opérations
        jobs_dict = {}
        for operation in inst._operations:
            job_id = operation.job_id
            if job_id not in jobs_dict:
                jobs_dict[job_id] = []
            jobs_dict[job_id].append(operation)
        
        # Créer les objets Job et les trier par ordre des opérations
        for job_id, operations_list in jobs_dict.items():
            # Trier les opérations par ID (supposant que l'ID reflète l'ordre)
            operations_list.sort(key=lambda op: op.operation_id)
            job = Job(job_id, operations_list)
            inst._jobs.append(job)
            inst._jobs_dict[job_id] = job
        
        # Trier les listes pour une cohérence
        inst._jobs.sort(key=lambda j: j.job_id)
        inst._machines.sort(key=lambda m: m.machine_id)
        inst._operations.sort(key=lambda op: op.operation_id)
        
        return inst

    @property
    def name(self) -> str:
        """Retourne le nom de l'instance."""
        return self._instance_name

    @property
    def machines(self) -> List[Machine]:
        """Retourne la liste des machines."""
        return self._machines.copy()  

    @property
    def jobs(self) -> List[Job]:
        """Retourne la liste des jobs."""
        return self._jobs.copy()  

    @property
    def operations(self) -> List[Operation]:
        """Retourne la liste des opérations."""
        return self._operations.copy()  

    @property
    def nb_jobs(self) -> int:
        """Retourne le nombre de jobs."""
        return len(self._jobs)

    @property
    def nb_machines(self) -> int:
        """Retourne le nombre de machines."""
        return len(self._machines)

    @property
    def nb_operations(self) -> int:
        """Retourne le nombre d'opérations."""
        return len(self._operations)

    def __str__(self) -> str:
        """Représentation en chaîne de l'instance."""
        return f"{self.name}_M{self.nb_machines}_J{self.nb_jobs}_O{self.nb_operations}"

    def get_machine(self, machine_id: int) -> Machine:
        """
        Retourne la machine avec l'ID spécifié.
        
        Args:
            machine_id (int): ID de la machine recherchée
            
        Returns:
            Machine: La machine correspondante
            
        Raises:
            KeyError: Si la machine n'existe pas
        """
        if machine_id not in self._machines_dict:
            raise KeyError(f"Machine with ID {machine_id} not found")
        return self._machines_dict[machine_id]

    def get_job(self, job_id: int) -> Job:
        """
        Retourne le job avec l'ID spécifié.
        
        Args:
            job_id (int): ID du job recherché
            
        Returns:
            Job: Le job correspondant
            
        Raises:
            KeyError: Si le job n'existe pas
        """
        if job_id not in self._jobs_dict:
            raise KeyError(f"Job with ID {job_id} not found")
        return self._jobs_dict[job_id]

    def get_operation(self, operation_id: int) -> Operation:
        """
        Retourne l'opération avec l'ID spécifié.
        
        Args:
            operation_id (int): ID de l'opération recherchée
            
        Returns:
            Operation: L'opération correspondante
            
        Raises:
            KeyError: Si l'opération n'existe pas
        """
        if operation_id not in self._operations_dict:
            raise KeyError(f"Operation with ID {operation_id} not found")
        return self._operations_dict[operation_id]
    
    def validate_instance(self) -> bool:
        """
        Valide la cohérence de l'instance.
        
        Returns:
            bool: True si l'instance est valide, False sinon
        """
        try:
            # Vérifier que toutes les machines référencées dans les opérations existent
            for operation in self._operations:
                for machine_id in operation.available_machines:
                    if machine_id not in self._machines_dict:
                        print(f"Warning: Operation {operation.operation_id} references non-existent machine {machine_id}")
                        return False
            
            # Vérifier que tous les jobs ont au moins une opération
            for job in self._jobs:
                if len(job.operations) == 0:
                    print(f"Warning: Job {job.job_id} has no operations")
                    return False
            
            # Vérifier la cohérence des données d'opération
            for operation in self._operations:
                if not operation.is_valid():
                    print(f"Warning: Operation {operation.operation_id} has inconsistent data")
                    return False
            
            return True
            
        except Exception as e:
            print(f"Error during instance validation: {e}")
            return False
    
    def get_operations_for_machine(self, machine_id: int) -> List[Operation]:
        """
        Retourne toutes les opérations qui peuvent être exécutées sur une machine donnée.
        
        Args:
            machine_id (int): ID de la machine
            
        Returns:
            List[Operation]: Liste des opérations compatibles avec cette machine
        """
        compatible_operations = []
        for operation in self._operations:
            if machine_id in operation.available_machines:
                compatible_operations.append(operation)
        return compatible_operations