from random import randrange
from math import sqrt
import matplotlib.pyplot as plt
from numpy import zeros
class cities_list:
    """a typical Traveling salesman problem"""
    __list=[]
    def __init__(self):
        return
    def __del__(self):
        return
    def add_city(self,x,y):
        """add a city location, this will be loaded into a list of cities"""
        num=coord(x,y)
        self.__list.append(num)
        return
    def get_list(self):
        return self.__list
    def set_list(self,tmplist):
        """set list of cities from existed list"""
        self.__list=tmplist
        return

    def display_cityinfo(self):
        """display location of cities"""
        print("list of city locations:")
        for i in range(len(self.__list)):
            print("city {0}: {1},{2}.".format(i+1,self.__list[i].x,self.__list[i].y))
    def shuffle_path(self):
        """shuffle list of coordinates to get possible solution using Sattolo's algorithm"""
        i=len(self.__list)
        while i>1:
            i-=1
            j=randrange(i)
            self.__list[i].x,self.__list[j].x=self.__list[j].x,self.__list[i].x
            self.__list[i].y,self.__list[j].y=self.__list[j].y,self.__list[i].y
        return
    def shuffle_path_m(self,list):
        """shuffle list to get possible solution using Sattolo's algorithm"""
        i=len(list)
        while i>1:
            i-=1
            j=randrange(i)
            list[i],list[j]=list[j],list[i]
        return list
    def calc_newSolution(self):
        """calculate total distance using euclidian distance"""
        newSolution=0
        for i in range(len(self.__list)-1):
            newSolution+=sqrt((self.__list[i].x-self.__list[i+1].x)*(self.__list[i].x-self.__list[i+1].x)+(self.__list[i].y-self.__list[i+1].y)*(self.__list[i].y-self.__list[i+1].y))
        newSolution+=sqrt((self.__list[0].x-self.__list[len(self.__list)-1].x)*(self.__list[0].x-self.__list[len(self.__list)-1].x)+(self.__list[0].y-self.__list[len(self.__list)-1].y)*(self.__list[0].y-self.__list[len(self.__list)-1].y))
        return newSolution

    def plot_location(self):
        """plot city location"""
        x_arr=zeros(len(self.__list))
        y_arr=zeros(len(self.__list))
        for i in range(len(self.__list)):
            x_arr[i]=self.__list[i].x
            y_arr[i]=self.__list[i].y
        plt.plot(x_arr,y_arr,'ro')
        plt.axis([0,100,0,100])
        plt.show()
        return
class coord:
        x=0
        y=0
        def __init__(self, h, v):
            self.x=h
            self.y=v


