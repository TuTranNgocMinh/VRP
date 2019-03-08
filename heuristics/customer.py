from location import location
from vehicle import vehicle
class customer:
    """package properties of each customer"""
    def __init__(self,id,name,quantity,volume,weight,address,deadline):
        self.id=id
        self.name=name
        self.quantity=quantity
        self.volume=volume
        self.weight=weight
        self.location=location(address)
        self.deadline=self.__convert(deadline)
        return
    def __convert(self,time):
        try:
            (h,m,s)=str(time).split(':')
            return int(h)*3600+int(m)*60+int(s)
        except:
            (h,m)=str(time).split(':')
            return int(h)*3600+int(m)*60
    def display(self):
        """display info of customer"""
        print("name: {0},quantity: {1}, volume: {2}, weight:{3},location: {4} deadline: {5}".format(self.name,self.quantity,self.volume,self.weight,self.location.coordinates,self.deadline))
        return
class DistributionCenter:
    """Distribution Center class for GA"""
    def __init__(self,address):
        self.__location=location(address)
        self.__VehicleList=[]
        return
    #get, set route for vehicle
    def getRoute(self,VPosition):
        return self.__VehicleList[VPosition].routing[:]
    def setRoute(self,routeList,VPosition):
        self.__VehicleList[VPosition].routing=routeList[:]
        return

    def getCoord(self):
        return self.__location.coordinates
    def addVehicle(self,Type,Volume,Weight,fuel_consumption=0):
        self.__VehicleList.append(vehicle(Type,Volume,Weight,fuel_consumption))
        return    
    def display(self):
        for i in range(len(self.__VehicleList)):
            print("Vehicle {0}:".format(i))
            self.__VehicleList[i].display()
        return




