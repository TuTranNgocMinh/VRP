class vehicle:
    """vehicle class. For fuel consumption, only specify if fuel cost is included"""
    def __init__(self,type,volume,weight,fuel_consumption=0):
        self.__type=type
        self.__volume=volume
        self.__weight=weight
        self.cost=0
        self.fuel_consumption=fuel_consumption
        self.routing=[]
        self.__TotalTimeTravelled=0
        self.__TotalDistanceTravelled=0
        self.__TotalHandling=0
        return
    def add_cost(self,cost):
        """specify cost if rent vehicle, none if own vehicle"""
        self.cost=cost
        return
    #property
    def getNumberofRoutes(self):
        return len(self.routing)
    #get,set total distance travelled
    def getTotalDistanceTravelled(self):
        return self.__TotalDistanceTravelled
    def setTotalDistanceTravelled(self,number):
        self.__TotalDistanceTravelled=number
        return
    #get,set total time travelled
    def getTotalTimeTravelled(self):
        return self.__TotalTimeTravelled
    def setTotalTimeTravelled(self,number):
        self.__TotalTimeTravelled=number
        return
    #get weight
    def getWeight(self):
        return self.__weight
    #get volume
    def getVolume(self):
        return self.__volume
    def display(self):
        """display info of vehicle"""
        print("name: {0}, volume: {1}, weight: {2}, cost: {3}, route: {4}"
              .format(self.type,self.volume,self.weight,self.cost,self.routing))
        return
class VehicleList:
    """this class is used whem import from vehicle table"""
    def __init__(self, type,volume,weight,quantity):
        self.__type=type
        self.__volume=volume
        self.__weight=weight
        self.__quantity=quantity
        return
    #property
    #get vehicle type
    def getType(self):
        return self.__type
    #get volume
    def getVolume(self):
        return self.__volume
    #get weight
    def getWeight(self):
        return self.__weight
    #get quantity
    def getQuantity(self):
        return self.__quantity