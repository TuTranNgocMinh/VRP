import googlemaps
import numpy as np
import math
class location:
    """description of class"""
    def __init__(self,address):
        client=googlemaps.Client('AIzaSyDV8WkL5FcxNXI7AGp83YnI6rLuaKuO7r0')
        self.Addr=address
        self.coordinates=client.geocode(self.Addr)
        self.coordinates=self.coordinates[0]['geometry']['location']
        return
    def __str__(self):
        return str(self.coordinates)
    def display(self):
        """display information of location"""
        print("Address: {0}".format(self.Addr))
        print("coordinates: {0}".format(self.coordinates))
        return

class dist_matrix:
    #__client=0
    #distance=0
    #time=0
    def __init__(self,origins,destinations):
        self.__origins=origins
        self.__destinations=destinations
        
        return
    def get_realdistance(self):
        """get distance matrix from origin points to destination points using google map API"""
        __client=googlemaps.Client('AIzaSyDV8WkL5FcxNXI7AGp83YnI6rLuaKuO7r0')
        matrix=__client.distance_matrix(self.__origins,self.__destinations)
        self.__distance=[[] for i in range(len(self.__destinations))]
        for i in range(len(self.__origins)):
            for j in range(len(self.__destinations)):
                self.__distance[i].append((matrix['rows'][i]['elements'][j]['distance']['value']))
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
    def getOriginsList(self):
        return self.__origins
    def getDestinationsList(self):
        return self.__destinations
    def getDistance(self):
        return self.__distance
    def display(self):
        print("origins: {0}".format(self.__origins))
        print("destinations: {0}".format(self.__destinations))
        print("distance matrix: {0}".format(self.__distance))
        print("time travel matrix: {0}".format(self.__time))
        return
