from location import location
from vehicle import vehicle
class customer:
    """package properties of each customer"""
    def __init__(self,id,name,quantity,volume,weight,address,deadline):
        self.__id=id
        self.__name=name
        self.__quantity=quantity
        self.__volume=volume
        self.__weight=weight
        self.location=address
        self.__deadline=self.__convert(deadline)
        return
    def __convert(self,time):
        try:
            (h,m,s)=str(time).split(':')
            return int(h)*3600+int(m)*60+int(s)
        except:
            (h,m)=str(time).split(':')
            return int(h)*3600+int(m)*60
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
        return self.location
    def display(self):
        """display info of customer"""
        print("name: {0},quantity: {1}, volume: {2}, weight:{3},location: {4} deadline: {5}".format(self.name,self.quantity,self.volume,self.weight,self.location.coordinates,self.deadline))
        return
class DistributionCenter:
    """Distribution Center class for GA"""
    def __init__(self,address,id):
        self.__location=address
        self.VehicleList=[]
        self.__id=id
        self.__TotalCost=0
        return
    #get id
    def getID(self):
        return self.__id
    #get, set route for vehicle
    def getRoute(self,VPosition):
        return self.VehicleList[VPosition].routing[:]
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
        return
    def getCoord(self):
        return self.__location
    #add vehicle
    def addVehicle(self,Type,Volume,Weight,fuel_consumption=0):
        self.VehicleList.append(vehicle(Type,Volume,Weight,fuel_consumption))
        return    
    def display(self):
        for i in range(len(self.VehicleList)):
            print("Vehicle {0}:".format(i))
            self.VehicleList[i].display()
        return




