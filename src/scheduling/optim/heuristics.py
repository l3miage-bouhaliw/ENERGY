'''
Mother class for heuristics.

@author: Vassilissa Lehoux
'''
from typing import Dict

from src.scheduling.instance.instance import Instance
from src.scheduling.solution import Solution


class Heuristic(object):
    '''
    classdocs
    '''

    def __init__(self, params: Dict=dict()):
        '''
        Constructor
        @param params: The parameters of your heuristic method if any as a
               dictionary. Implementation should provide default values in the function.
        '''
        raise "Not Implemented Error"

    def run(self, instance: Instance, params: Dict=dict()) -> Solution:
        '''
        Computes a solution for the given instance.
        Implementation should provide default values in the function
        (the function will be evaluated with an empty dictionary).
        @param instance: the instance to solve
        @param params: the parameters for the run
        '''
        raise "Not Implemented Error"
        
