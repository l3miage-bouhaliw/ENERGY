'''
Heuristics that compute an initial solution and 
then improve it.

@author: Vassilissa Lehoux
'''
from typing import Dict

from src.scheduling.optim.heuristics import Heuristic
from src.scheduling.instance.instance import Instance
from src.scheduling.solution import Solution
from src.scheduling.optim.constructive import NonDeterminist
from src.scheduling.optim.neighborhoods import MyNeighborhood1


class FirstNeighborLocalSearch(Heuristic):
    '''
    Vanilla local search will first create a solution,
    then at each step try and improve it by looking at
    solutions in its neighborhood.
    The first solution found that improves over the current solution
    replaces it.
    The algorithm stops when no solution is better than the current solution
    in its neighborhood.
    '''

    def __init__(self, params: Dict=dict()):
        '''
        Constructor
        @param params: The parameters of your heuristic method if any as a
               dictionary. Implementation should provide default values in the function.
        '''
        raise "Not implemented error"

    def run(self, instance: Instance, InitClass, NeighborClass, params: Dict=dict()) -> Solution:
        '''
        Compute a solution for the given instance.
        Implementation should provide default values in the function
        (the function will be evaluated with an empty dictionary).

        @param instance: the instance to solve
        @param InitClass: the class for the heuristic computing the initialization
        @param NeighborClass: the class of neighborhood used in the vanilla local search
        @param params: the parameters for the run
        '''
        raise "Not implemented error"


class BestNeighborLocalSearch(Heuristic):
    '''
    Vanilla local search will first create a solution,
    then at each step try and improve it by looking at
    solutions in its neighborhood.
    The best solution found that improves over the current solution
    replaces it.
    The algorithm stops when no solution is better than the current solution
    in its neighborhood.
    '''

    def __init__(self, params: Dict=dict()):
        '''
        Constructor
        @param params: The parameters of your heuristic method if any as a
               dictionary. Implementation should provide default values in the function.
        '''
        raise "Not implemented error"

    def run(self, instance: Instance, InitClass, NeighborClass, params: Dict=dict()) -> Solution:
        '''
        Computes a solution for the given instance.
        Implementation should provide default values in the function
        (the function will be evaluated with an empty dictionary).

        @param instance: the instance to solve
        @param InitClass: the class for the heuristic computing the initialization
        @param NeighborClass: the class of neighborhood used in the vanilla local search
        @param params: the parameters for the run
        '''
        raise "Not implemented error"


if __name__ == "__main__":
    # To play with the heuristics
    from src.scheduling.tests.test_utils import TEST_FOLDER_DATA
    import os
    inst = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp10")
    heur = FirstNeighborLocalSearch()
    sol = heur.run(inst, NonDeterminist, MyNeighborhood1)
    plt = sol.gantt("tab20")
    plt.savefig("gantt.png")
