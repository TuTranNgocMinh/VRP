import copy
import math
import numpy as np
import random
class model_GA(object):
    """description of class"""
    def __init__(self,CustomerList,VehicleList,DistanceObject,DCList,VehicleRank,DistanceRank):
        self.__CustomerList=CustomerList
        self.__VehicleList=VehicleList
        self.__DistanceMatrix=DistanceObject.getDistance()
        self.__TimeMatrix=DistanceObject.getTime()     
        self.__DCList=DCList
        self.__VRank=VehicleRank
        self.__DRank=DistanceRank
        return
    def initpopulation(self,population,LocGroup):
        self.__population=[]
        #find array with max elements
        max=0
        for i in range(len(LocGroup)):
            if (len(LocGroup[i])>len(LocGroup[max])):
                max=i
        #create population
        for num in range(population):
            #print("population {0}".format(num))
            temp=[]
            #create weight and volume variable
            weight=np.zeros(len(LocGroup))
            volume=np.zeros(len(LocGroup))
            self.__population.append(copy.deepcopy(self.__DCList))
            #add vehicle to all DCs
            for i in range(len(LocGroup)):
                self.__population[num][i].addVehicle(
                    self.__VehicleList[0][0],self.__VehicleList[0][1],self.__VehicleList[0][2],self.__VehicleList[0][3])
                temp.append(0)
            LocCopy=copy.deepcopy(LocGroup)
            while(len(LocCopy[max])>0):
                for i in range(len(LocCopy)):
                    if (LocCopy[i]):
                        rand=random.randrange(0,len(LocCopy[i]))
                        #calculate weight and volume
                        weight[i]=weight[i]+LocCopy[i][rand].getWeight()*LocCopy[i][rand].getQuantity()
                        volume[i]=volume[i]+LocCopy[i][rand].getVolume()*LocCopy[i][rand].getQuantity()
                        #check condition. If true,add route. Else, reset weight and volume to last customer and add vehicle
                        if ((weight[i]<=self.__VehicleList[0][2])and(volume[i]<=90*self.__VehicleList[0][1]/100)):
                            self.__population[num][i].appendRoute(temp[i],LocCopy[i][rand])
                        else:
                            self.__population[num][i].addVehicle(
                    self.__VehicleList[0][0],self.__VehicleList[0][1],self.__VehicleList[0][2],self.__VehicleList[0][3])
                            temp[i]=temp[i]+1 #increase temp variable by 1
                            #print("DC {0}: {1}".format(i,temp[i]))
                            self.__population[num][i].appendRoute(temp[i],LocCopy[i][rand])
                            #reset weight and volume
                            weight[i]=LocCopy[i][rand].getWeight()*LocCopy[i][rand].getQuantity()
                            volume[i]=LocCopy[i][rand].getVolume()*LocCopy[i][rand].getQuantity()
                        #delete temp Customer
                        del LocCopy[i][rand]
            #test route
            for k in range(len(LocGroup)):
                number=self.__population[num][k].GetNumberVehicles()
                #print("number of vehicle in DC {0}: {1}".format(k,number))
                TotalCost=self.__VRank*number #total cost of DC,number of vehicle cost
                VCost=0 #total traveling distance cost of DC
                for vehicle in range(number):                    
                    NumberofRoutes=self.__population[num][k].VehicleList[vehicle].getNumberofRoutes()
                    #for route in range(NumberofRoutes):
                        #print("route {0} vehicle {1} DC {2}: {3}".format(route,vehicle,k,self.__population[num][k].VehicleList[vehicle].routing[route].getID()))
                    Vehicle=self.__population[num][k].VehicleList[vehicle]
                    self.DistanceCalculation(k,Vehicle)
                    #print("Distance: {0}".format(Vehicle.getTotalDistanceTravelled()))
                    #total cost calculation
                    VCost+=self.__population[num][k].VehicleList[vehicle].getTotalDistanceTravelled()
                TotalCost+=VCost*self.__DRank
                self.__population[num][k].setTotalCost(TotalCost)
                #print("Total Cost of DC {0}: {1}".format(k,self.__population[num][k].getTotalCost()))
        return
    def initGroup(self):
        if (len(self.__DCList)>1):
            #create Loc Group list
            LocGroup=[]
            for i in self.__DCList:
                LocGroup.append([])
            #create DC to location distance matrix
            maxIndex=len(self.__DistanceMatrix[0])
            DC_Distance=self.__DistanceMatrix[maxIndex-len(self.__DCList):maxIndex,:]
            #find minimum distance of each DC
            for j in range(len(self.__CustomerList)):
                array=np.zeros(len(DC_Distance))
                for i in range(len(DC_Distance)):
                    array[i]=DC_Distance[i][j]
                min=np.argmin(array)
                LocGroup[min].append(self.__CustomerList[j])
        return copy.deepcopy(LocGroup)
    def Mutation(self,individuals):
        #get random DC index
        rand=random.randrange(0,len(self.__DCList))
        #get random vehicle index
        Vrd=random.randrange(0,individuals[rand].GetNumberVehicles())
        #get random number of route index in each of that vehicle
        rd1=random.randrange(0,len(individuals[rand].VehicleList[Vrd].routing))
        rd2=random.randrange(0,len(individuals[rand].VehicleList[Vrd].routing))
        while(rd1==rd2):
            Vrd=random.randrange(0,individuals[rand].GetNumberVehicles())
            rd1=random.randrange(0,len(individuals[rand].VehicleList[Vrd].routing))
            rd2=random.randrange(0,len(individuals[rand].VehicleList[Vrd].routing))
            
        #define list1,list2
        list=individuals[rand].VehicleList[Vrd].routing     
        self.__swap(rd1,rd2,list,list)
        #print changes
        #print("")
        #print("DC chosen: {0}".format(rand))
        number=individuals[rand].GetNumberVehicles()
        TotalCost=self.__VRank*number #total cost of DC,number of vehicle cost
        VCost=0 #total traveling distance cost of DC
        for vehicle in range(number):
            NumberofRoutes=individuals[rand].VehicleList[vehicle].getNumberofRoutes()
            #for route in range(NumberofRoutes):
                #print("route {0} vehicle {1} DC {2}: {3}".format(
                #route,vehicle,rand,individuals[rand].VehicleList[vehicle].routing[route].getID()))
            Vehicle=individuals[rand].VehicleList[vehicle]
            self.DistanceCalculation(rand,Vehicle)
            VCost+=individuals[rand].VehicleList[vehicle].getTotalDistanceTravelled()
            #print("Distance: {0}".format(Vehicle.getTotalDistanceTravelled()))
        TotalCost+=VCost*self.__DRank
        individuals[rand].setTotalCost(TotalCost)
        #print("total cost: {0}".format(individuals[rand].getTotalCost()))
        return 
    def crossover(self,parent1,parent2): #not tested yet
        #print("__________________________________________")
        #print("crossover: ")
        self.__children=[]
        #copy 2 parents
        child1=copy.deepcopy(self.__population[parent1])
        child2=copy.deepcopy(self.__population[parent2])
        self.__children.append(child1)
        self.__children.append(child2)
        flag1=True
        flag2=True
        #perform crossover func
        for DCIndex in range(len(self.__DCList)):
            vrd1=random.randrange(0,len(child1[DCIndex].VehicleList))
            vrd2=random.randrange(0,len(child2[DCIndex].VehicleList))
            route1=child1[DCIndex].VehicleList[vrd1]
            route2=child2[DCIndex].VehicleList[vrd2]

            if(self.crossover_func(child1[DCIndex],DCIndex,route2,vrd2)==True):
                number=child1[DCIndex].GetNumberVehicles()
                TotalCost=self.__VRank*number #total cost of DC,number of vehicle cost
                VCost=0 #total traveling distance cost of DC
                for vehicle in range(child1[DCIndex].GetNumberVehicles()):
                    self.DistanceCalculation(DCIndex,child1[DCIndex].VehicleList[vehicle])
                    VCost+=child1[DCIndex].VehicleList[vehicle].getTotalDistanceTravelled()
                TotalCost+=self.__DRank*VCost
                child1[DCIndex].setTotalCost(TotalCost)
            else:
                flag1=False
            if(self.crossover_func(child2[DCIndex],DCIndex,route1,vrd1)==True):
                number=child2[DCIndex].GetNumberVehicles()
                TotalCost=self.__VRank*number #total cost of DC,number of vehicle cost
                VCost=0 #total traveling distance cost of DC
                for vehicle in range(child2[DCIndex].GetNumberVehicles()):
                    VCost+=self.DistanceCalculation(DCIndex,child2[DCIndex].VehicleList[vehicle])
                TotalCost+=self.__DRank*VCost
                child2[DCIndex].setTotalCost(TotalCost)
            else:
                flag2=False
        if(flag1==False):
            del self.__children[0]
        elif(flag2==False):
            del self.__children[1]
        elif(flag1==False)and(flag2==False):
            self.deleteChildren()
        return
    def Selection(self,threshold):
        randpop1=random.randrange(0,len(self.__population))
        randpop2=random.randrange(0,len(self.__population))
        while(randpop1==randpop2):
            randpop2=random.randrange(0,len(self.__population))
        #choose fittest parent
        Min=self.MinIndex(self.__population[randpop1],self.__population[randpop2])
        rand=random.uniform(0,1)
        if(rand<=threshold):
            if(Min==0):
                return randpop1
            else:
                return randpop2
        else:
            candidates=[randpop1,randpop2]
            rIndex=random.choice(candidates)
            return rIndex
        return
    def SurvivorSelection(self):
        for index in range(len(self.__children)):
            max=self.Max()
            #print("population with largest cost: {0}".format(max))
            del self.__population[max]
        for index in range(len(self.__children)):
            self.__population.append(copy.deepcopy(self.__children[index]))
    #modifying function    
    def crossover_func(self,DC,DCIndex,Vehicle,VIndex): #not tested yet
        #remove customers from parent 2's route
        CustomerCopy=[]
        #print("DC Index: {0}".format(DCIndex))
        for customers in range(len(Vehicle.routing)):
            self.FindandRemove(CustomerCopy,DC,Vehicle,customers)
            #print("Customer list copy: {0}".format(CustomerCopy[customers].getID()))
            #insert            
        for customer in range(len(CustomerCopy)):
            SortedFList=[]
            for vehicle in range(len(DC.VehicleList)):
                #print("vehicle length of DC {0}: {1}".format(DCIndex,len(DC.VehicleList[vehicle].routing)))
                if (len(DC.VehicleList[vehicle].routing)==0)and(len(DC.VehicleList)==1):
                    SortedFList.append({'Position':0,'vIndex': vehicle ,'Cost': 0,'feasible':True})
                    break
                for Position in range(len(DC.VehicleList[vehicle].routing)+1):
                    DC.VehicleList[vehicle].routing.insert(Position,CustomerCopy[customer])                   
                    totalDistance=self.DistanceCalculation(DCIndex,DC.VehicleList[vehicle])
                    weight,vol=self.ConstraintCalculation(DC.VehicleList[vehicle])
                    if(self.checkCondition(weight,vol,DC.VehicleList[vehicle])==True):
                        SortedFList.append({'Position':Position,'vIndex': vehicle ,'Cost': totalDistance,'feasible':True})
                    else:
                        SortedFList.append({'Position':Position,'vIndex': vehicle ,'Cost': totalDistance,'feasible':False})
                    del DC.VehicleList[vehicle].routing[Position]

            SortedFList.sort(key=lambda k: k['Cost'])
            #print("")
            #print("sorted feasible List: {0}".format(SortedFList))
            k=random.uniform(0,1)
            #print("random number: {0}".format(k))
            if (k<=0.8):
                for i in range(len(SortedFList)):
                    if(SortedFList[i]['feasible']==True):
                        vIndex=SortedFList[i]['vIndex']
                        rIndex=SortedFList[i]['Position']
                        DC.VehicleList[vIndex].routing.insert(rIndex,CustomerCopy[customer])
                        break
            else:
                vIndex=SortedFList[0]['vIndex']
                rIndex=SortedFList[0]['Position']
                DC.VehicleList[vIndex].routing.insert(rIndex,CustomerCopy[customer])
                if(SortedFList[0]['feasible']==False):
                    return False
        return True
    def FindandRemove(self,CustomerCopy,DC,Vehicle,CustomerIndex):
        for vehicle in range(DC.GetNumberVehicles()):
            routes=len(DC.VehicleList[vehicle].routing)
            for PCustomers in range(routes):
                if(DC.VehicleList[vehicle].routing[PCustomers].getID()==Vehicle.routing[CustomerIndex].getID()):
                    CustomerCopy.append(copy.deepcopy(DC.VehicleList[vehicle].routing[PCustomers]))
                    del DC.VehicleList[vehicle].routing[PCustomers]
                    return
        return
    #calculating function
    def DistanceCalculation(self,dcIndex,vehicle):     
        """calculate distance based on vehicle object""" 
        totalDistanceTraveled=0
        DCID=self.__DCList[dcIndex].getID()            
        totalDistanceTraveled+=self.__DistanceMatrix[DCID][vehicle.routing[0].getID()]
        for j in range(len(vehicle.routing)-1):
            totalDistanceTraveled+=self.__DistanceMatrix[vehicle.routing[j].getID()][vehicle.routing[j+1].getID()]
        totalDistanceTraveled+=self.__DistanceMatrix[vehicle.routing[len(vehicle.routing)-1].getID()][DCID]
        vehicle.setTotalDistanceTravelled(totalDistanceTraveled)
        return totalDistanceTraveled
    def ConstraintCalculation(self,vehicle): 
        """Recalculate weight and volume of route in a vehicle"""
        weight=0
        vol=0
        for customer in range(len(vehicle.routing)):
            weight+=vehicle.routing[customer].getWeight()*vehicle.routing[customer].getQuantity()
            vol+=vehicle.routing[customer].getVolume()*vehicle.routing[customer].getQuantity()
        return weight,vol
    def __swap(self,a,b,list1,list2):
        list1[a],list2[b]=list2[b],list1[a]
        return 
    def __sum(a,b):
        return a+b
    #modifying function
    def deleteChildren(self):
        for i in range(len(self.__children)):
            del self.__children[0]
        return
    def MinIndex(self,candidate1,candidate2):
        TotalCost1=0
        TotalCost2=0
        for DCIndex in range(len(self.__DCList)):
            TotalCost1+=candidate1[DCIndex].getTotalCost()
            TotalCost2+=candidate2[DCIndex].getTotalCost()
        if(TotalCost1<TotalCost2):
            return 0
        else: 
            return 1
        return
    def Max(self):        
        MaxValue=0
        MaxIndex=0
        for i in range(len(self.__population)):
            TotalCost=0
            for DCIndex in range(len(self.__DCList)):
                TotalCost+=self.__population[i][DCIndex].getTotalCost()
            if(TotalCost>MaxValue):
                MaxValue=TotalCost
                MaxIndex=i
        return MaxIndex
    #check constraint functions
    def checkCondition(self,Rweight,Rvolume,Vehicle): #not tested yet
        volume=90*Vehicle.getVolume()/100
        if(Rweight<=Vehicle.getWeight())and(Rvolume<=volume):
            return True
        else:
            return False
    #display function
    def display(self):
        for num in range(len(self.__population)):
            print("population {0}".format(num))
            for DCIndex in range(len(self.__DCList)):
                print("Distribution Center {0}".format(DCIndex))
                for vehicle in range(self.__population[num][DCIndex].GetNumberVehicles()):
                    for customer in range(self.__population[num][DCIndex].VehicleList[vehicle].getNumberofRoutes()):
                        print("vehicle {0}: {1}".format(
                            vehicle,self.__population[num][DCIndex].VehicleList[vehicle].routing[customer].getID()))
                    print("total distance travelled: {0}".format(
                        self.__population[num][DCIndex].VehicleList[vehicle].getTotalDistanceTravelled()))
                print("Total cost: {0}".format(self.__population[num][DCIndex].getTotalCost()))
        print("")
        for num in range(len(self.__children)):
            print("child {0}".format(num))
            for DCIndex in range(len(self.__DCList)):
                print("Distribution Center {0}".format(DCIndex))
                for vehicle in range(self.__children[num][DCIndex].GetNumberVehicles()):
                    for customer in range(self.__children[num][DCIndex].VehicleList[vehicle].getNumberofRoutes()):
                        print("vehicle {0}: {1}".format(
                            vehicle,self.__children[num][DCIndex].VehicleList[vehicle].routing[customer].getID()))
                    print("total distance travelled: {0}".format(
                    self.__children[num][DCIndex].VehicleList[vehicle].getTotalDistanceTravelled()))
                print("Total cost: {0}".format(self.__children[num][DCIndex].getTotalCost()))
        return
    #main loop function
    def mainloop(self,maxIter,threshold):
        for i in range(maxIter):
            parent1=self.Selection(0.8)
            parent2=self.Selection(0.8)
            while(parent1==parent2):
                parent2=self.Selection(0.8)
            #print("parent 1 chosen: {0}".format(parent1))
            #print("parent 2 chosen: {0}".format(parent2))
            rand=random.uniform(0,1)
            if(rand<=0.85):
                self.crossover(parent1,parent2)
            else:
                self.__children=[]
                self.__children.append(copy.deepcopy(self.__population[parent1]))
                self.__children.append(copy.deepcopy(self.__population[parent2]))
            #print("_______________________________________")
            for popIndex in range(len(self.__population)):
                rand=random.uniform(0,1)
                if(rand>0.9):
                    self.Mutation(self.__population[popIndex])
            for popIndex in range(len(self.__children)):
                rand=random.uniform(0,1)
                if(rand>0.9):
                    self.Mutation(self.__children[popIndex])
            self.display()            
            self.SurvivorSelection()
            self.deleteChildren()
            self.display()
