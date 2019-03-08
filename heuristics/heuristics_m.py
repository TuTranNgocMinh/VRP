class heuristics_m:
    """master formula for heuristics algorithm"""
    __currentSolution=0
    __bestSolution=100000000
    def __init__(self):
        return
    def __del__(self):
        return

    def set_current(self,current_var):
        """set current solution"""
        self.__currentSolution=current_var
        return
    def get_current(self):
        """get current solution"""
        return self.__currentSolution

    def set_best(self,best_solution):
        """set best solution"""
        self.__bestSolution=best_solution
        return
    def get_best(self):
        """get best solution"""
        return self.__bestSolution

class coord:
    """coordinate"""
    x=0
    y=0
    def __init__(self, h, v):
        self.x=h
        self.y=v
        return
class var_n:
    """variable object"""
    