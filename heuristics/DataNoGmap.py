from vehicle import vehicle
import numpy as np
import math
class CustomerNoGmap:
    """description of class"""
    """package properties of each customer"""
    def __init__(self,id,name,quantity,volume,weight,location):
        self.__id=id
        self.__name=name
        self.__quantity=quantity
        self.__volume=volume
        self.__weight=weight
        self.__location=location
        return
    #get id
    def getID(self):
        return self.__id
    #get quantity
    def getQuantity(self):
        return self.__quantity
    #get volume
    def getVolume(self):
        return self.__volume
    #get weight
    def getWeight(self):
        return self.__weight
    #get location
    def getLocation(self):
        return self.__location
    def display(self):
        """display info of customer"""
        print("name: {0},quantity: {1}, volume: {2}, weight:{3},location: {4}"
              .format(self.__name,self.__quantity,self.__volume,self.__weight,self.__location))
        return
class DCNoGmap:
    """Distribution Center class for GA"""
    def __init__(self,location,id):
        self.__location=location
        self.VehicleList=[]
        self.__id=id
        self.__TotalCost=0
        return
    #get id
    def getID(self):
        return self.__id
    #add vehicle
    def addVehicle(self,Type,Volume,Weight,fuel_consumption=0):
        self.VehicleList.append(vehicle(Type,Volume,Weight,fuel_consumption))
        return
    def GetNumberVehicles(self):
        return len(self.VehicleList)
    #get, set route for vehicle
    def getRoute(self,VPosition):
        return self.VehicleList[VPosition].routing
    def setRoute(self,routeList,VPosition):
        self.VehicleList[VPosition].routing=routeList[:]
        return
    def appendRoute(self,VPosition,route):
        self.VehicleList[VPosition].routing.append(route)
        return
    #get, set Total Cost
    def getTotalCost(self):
        return self.__TotalCost
    def setTotalCost(self,TotalCost):
        self.__TotalCost=TotalCost
    def getCoord(self):
        return self.__location.copy()
           
    def display(self):
        for i in range(len(self.VehicleList)):
            print("Vehicle {0}:".format(i))
            self.VehicleList[i].display()
        return
class DistMatrixNoGmap:
    """class contains distance matrix and time travelled matrix for VRP"""
    def __init__(self,origins,destinations):
        self.__origins=origins
        self.__destinations=destinations
        self.__distance=0
        self.__time=0
        return
    def __haversine(self,lat2,lat1,lng2,lng1):
        dlng = lng2 - lng1
        dlat = lat2 - lat1
        R=6373 #radius of earth in km
        a = (math.sin(math.radians(dlat/2)))**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * ((math.sin(math.radians(dlng/2)))**2) 
        c = 2 * math.atan2( math.radians(math.sqrt(a)), math.radians(math.sqrt(1-a)))
        d = R * c
        return d
    def get_approxdistance(self):
        """get distance matrix origin points to destination points using approximate calculation.\n Algorithm used: Haversine"""
        self.__distance=np.zeros((len(self.__origins),len(self.__destinations)))
        self.__time=np.zeros((len(self.__origins),len(self.__destinations))) #maximum speed: 40 km/h
        for i in range(len(self.__origins)):
            for j in range(len(self.__destinations)):
                self.__distance[i][j]=self.__haversine(self.__destinations[j]['lat'],self.__origins[i]['lat'],
                                                     self.__destinations[j]['lng'],self.__origins[i]['lng'])
                self.__time[i][j]=self.__distance[i][j]/40
        return
    #Get origin list
    def getOriginsList(self):
        return self.__origins[:]
    #get Destination list
    def getDestinationsList(self):
        return self.__destinations[:]
    #get distance matrix
    def getDistance(self):
        return self.__distance
    #get time matrix
    def getTime(self):
        return self.__time
    def display(self):
        print("origins: {0}".format(self.__origins))
        print("destinations: {0}".format(self.__destinations))
        print("distance matrix: {0}".format(self.__distance))
        print("time travel matrix: {0}".format(self.__time))
        return