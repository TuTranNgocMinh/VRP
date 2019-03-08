import heuristics_m
class Tabu_Search:
    """declaration"""
    __tabu_list=[]
    h=heuristics_m.heuristics_m()
    def __init__(self,n_tabu):
        for i in range(n_tabu):
            self.__tabu_list[i].append([0,0])
        return
    def display_info(self):
        """display tabu list"""
        print("current solution:{0}".format(self.h.get_current()))
        print("best solution:{0}".format(self.h.get_best()))
        return
    def ismatch(self,exchange_list):
        """check if pairwise exchange list match with tabu list"""
        for i in range(len(self.__tabu_list)):
            if self.__tabu_list[i]==exchange_list:
                return True
        return False    
    def set_tabu(self,iter,exchange_list):
        """set tabu in coordinates,iteration must started at 0 and ends at number of tabu list-1"""
        self.__tabu_list[iter]=exchange_list
        return