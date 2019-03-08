from random import betavariate
from math import exp


class Simmulated_Annealing:
    """declaration"""
    __temp=0
    __currentSolution=0
    __bestSolution=100000000
    def __init__(self):
        self.__temp=1000
    def __del__(self):
        return

    def set_temp(self,temperature):
        """set initial temperature. Default: temp=1000"""
        self.__temp=temperature
        return
    def get_temp(self):
        """get current temperature"""
        return self.__temp

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

    def shuffle_path(self,list):
        """shuffle list to get possible solution using Sattolo's algorithm"""
        i=len(list)
        while i>1:
            i-=1
            j=randrange(i)
            list[i],list[j]=list[j],list[i]
        return list

    def shuffle_path(self,list):
        """shuffle list of coordinates to get possible solution using Sattolo's algorithm"""
        i=len(list)
        while i>1:
            i-=1
            j=randrange(i)
            list[i].x,list[j].x=list[j].x,list[i].x
            list[i].y,list[j].y=list[j].y,list[i].y
        return

    def calculate(self,newSolution,desc_rate):
        """keep new solution if neighour energy < current energy, 
        if neighbour energy > current energy it will have a probability to accept new solution"""
        energy=newSolution-self.__currentSolution
        if energy<0:
            self.__temp*=(1-desc_rate)
            return True
        probability=exp(-(energy)/self.__temp)
        threshold=betavariate(0.5,0.5)
        self.__temp*=(1-desc_rate)
        return True if probability>threshold else False
    def display_info(self):
        print("\ncurrent solution: {0}".format(self.__currentSolution))
        print("temperature: {0}".format(self.__temp))
        print("best solution: {0}".format(self.__bestSolution))
        return