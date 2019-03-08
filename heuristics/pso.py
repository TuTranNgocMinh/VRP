import heuristics_m as h
from random import uniform
class pso:
    """particle swarm optimization"""
    __gbest=10000000
    __pbest=0
    __current=0
    c=h.heuristics_m()
    def __init__(self):
        return
    def set_gbest(self,global_best):
        self.__gbest=global_best
        return
    def get_gbest(self):
        return self.__gbest
