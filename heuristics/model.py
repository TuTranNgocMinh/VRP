import copy
import math
import numpy as np
import random
class Solution(object):
    """Solution container for model"""
    def __init__(self,DCList):
        self.DC=DCList
        self.__TotalCost=0
    #get, set total cost
    def setTotalCost(self):
        TotalCost=0
        for DCIndex in range(len(self.DC)):
            TotalCost+=self.DC[DCIndex].getTotalCost()
        self.__TotalCost=TotalCost
    def getTotalCost(self):
        return self.__TotalCost
    #get number of DC
    def getDCNumber(self):
        return len(self.DC)
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
        self.__bestSolution={'Value':1000000,'route':0}
        return
    #get best solution
    def getBestSolution(self):
        return copy.deepcopy(self.__bestSolution['route'])
    def getBestValue(self):
        return copy.deepcopy(self.__bestSolution['Value'])
    def initpopulation(self,population,LocGroup):
        self.__population=[]
        #find array with max elements
        max=0
        for i in range(len(LocGroup)):
            if (len(LocGroup[i])>len(LocGroup[max])):
                max=i
        #create population
        for num in range(population):
            vnumber=[]
            #create weight and volume variable
            weight=np.zeros(len(LocGroup))
            volume=np.zeros(len(LocGroup))
            self.__population.append(Solution(copy.deepcopy(self.__DCList)))
            #add vehicle to all DCs
            for i in range(len(LocGroup)):
                self.__population[num].DC[i].addVehicle(
                    self.__VehicleList[0][0],self.__VehicleList[0][1],self.__VehicleList[0][2],self.__VehicleList[0][3])
                vnumber.append(0)
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
                            self.__population[num].DC[i].appendRoute(vnumber[i],LocCopy[i][rand])
                        else:
                            self.__population[num].DC[i].addVehicle(
                    self.__VehicleList[0][0],self.__VehicleList[0][1],self.__VehicleList[0][2],self.__VehicleList[0][3])
                            vnumber[i]=vnumber[i]+1 #increase vnumber variable by 1
                            self.__population[num].DC[i].appendRoute(vnumber[i],LocCopy[i][rand])
                            #reset weight and volume
                            weight[i]=LocCopy[i][rand].getWeight()*LocCopy[i][rand].getQuantity()
                            volume[i]=LocCopy[i][rand].getVolume()*LocCopy[i][rand].getQuantity()
                        #delete vnumber Customer
                        del LocCopy[i][rand]
            #test route
            for k in range(len(LocGroup)):
                number=self.__population[num].DC[k].GetNumberVehicles()
                TotalCost=self.__VRank*number*5000
                for vehicle in range(number):                    
                    Vehicle=self.__population[num].DC[k].VehicleList[vehicle]
                    self.DistanceCalculation(k,Vehicle)
                    #total cost calculation
                    TotalCost+=self.__population[num].DC[k].VehicleList[vehicle].getTotalDistanceTravelled()*self.__DRank
                self.__population[num].DC[k].setTotalCost(TotalCost)
            self.__population[num].setTotalCost()
        return
    def initGroup(self):
        LocGroup=[]
        if (len(self.__DCList)>1):
            #create Loc Group list            
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
        else:
            LocGroup.append([])
            for j in range(len(self.__CustomerList)):
                LocGroup[0].append(self.__CustomerList[j])
        return copy.deepcopy(LocGroup)
    def Mutation(self,individuals):
        #get random DC index
        rand=random.randrange(0,len(self.__DCList))
        #while the chosen DC has only 1 vehicle with 1 route or no vehicle
        while(((individuals.DC[rand].GetNumberVehicles()==1)and(individuals.DC[rand].VehicleList[0].getNumberofRoutes()==1))or(individuals.DC[rand].GetNumberVehicles()==0)):
            rand=random.randrange(0,len(self.__DCList))
        #get random vehicle index
        Vrd1=random.randrange(0,individuals.DC[rand].GetNumberVehicles())
        Vrd2=random.randrange(0,individuals.DC[rand].GetNumberVehicles())
        #get random number of route index in each of that vehicle
        rd1=random.randrange(0,len(individuals.DC[rand].VehicleList[Vrd1].routing))
        rd2=random.randrange(0,len(individuals.DC[rand].VehicleList[Vrd2].routing))
        while(rd1==rd2)and(Vrd1==Vrd2):
            Vrd2=random.randrange(0,individuals.DC[rand].GetNumberVehicles())
            rd2=random.randrange(0,len(individuals.DC[rand].VehicleList[Vrd2].routing))
        #define list1,list2
        list1=individuals.DC[rand].VehicleList[Vrd1].routing
        list2=individuals.DC[rand].VehicleList[Vrd2].routing     
        self.__swap(rd1,rd2,list1,list2)
        #print changes
        number=individuals.DC[rand].GetNumberVehicles()
        TotalCost=self.__VRank*number*5000
        for vIndex in range(number):
            weight,vol=self.ConstraintCalculation(individuals.DC[rand].VehicleList[vIndex])
            if(self.checkCondition(weight,vol,individuals.DC[rand].VehicleList[vIndex])==False):
                return False
            Vehicle=individuals.DC[rand].VehicleList[vIndex]
            self.DistanceCalculation(rand,Vehicle)
            TotalCost+=individuals.DC[rand].VehicleList[vIndex].getTotalDistanceTravelled()*self.__DRank
        individuals.DC[rand].setTotalCost(TotalCost)
        individuals.setTotalCost()
        return True
    def crossover(self,parent1,parent2):
        self.__children=[]
        #choose random DC
        DC=random.randrange(0,len(self.__DCList))
        #copy 2 parents
        child1=copy.deepcopy(self.__population[parent1])
        child2=copy.deepcopy(self.__population[parent2])
        self.__children.append(child1)
        self.__children.append(child2)
        flag1=True
        flag2=True
        #perform crossover func
        vrd1=random.randrange(0,len(child1.DC[DC].VehicleList))
        vrd2=random.randrange(0,len(child2.DC[DC].VehicleList))
        route1=child1.DC[DC].VehicleList[vrd1]
        route2=child2.DC[DC].VehicleList[vrd2]

        if(self.crossover_func(child1.DC[DC],DC,route2,vrd2)==True):
            number=child1.DC[DC].GetNumberVehicles()
            TotalCost=self.__VRank*number*5000
            for vehicle in range(number):
                self.DistanceCalculation(DC,child1.DC[DC].VehicleList[vehicle])
                TotalCost+=child1.DC[DC].VehicleList[vehicle].getTotalDistanceTravelled()*self.__DRank
            child1.DC[DC].setTotalCost(TotalCost)
            child1.setTotalCost()
        else:
            flag1=False
        if(self.crossover_func(child2.DC[DC],DC,route1,vrd1)==True):
            number=child2.DC[DC].GetNumberVehicles()
            TotalCost=self.__VRank*number*5000
            for vehicle in range(number):
                self.DistanceCalculation(DC,child2.DC[DC].VehicleList[vehicle])
                TotalCost+=child2.DC[DC].VehicleList[vehicle].getTotalDistanceTravelled()*self.__DRank
            child2.DC[DC].setTotalCost(TotalCost)
            child2.setTotalCost()
        else:
            flag2=False
        if(flag1==False)and(flag2==False):
            self.deleteChildren()
        elif(flag2==False):
            del self.__children[1]
        elif(flag1==False):
            del self.__children[0]
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
            del self.__population[max]
        for index in range(len(self.__children)):
            self.__population.append(copy.deepcopy(self.__children[index]))
    #modifying function    
    def crossover_func(self,DC,DCIndex,Vehicle,VIndex):
        #remove customers from parent 2's route
        CustomerCopy=[]
        for customers in range(len(Vehicle.routing)):
            self.FindandRemove(CustomerCopy,DC,Vehicle,customers)
            #insert            
        for customer in range(len(CustomerCopy)):
            SortedFList=[]
            for vehicle in range(len(DC.VehicleList)):
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
            k=random.uniform(0,1)
            if (k<=0.8):
                feasible=False
                for i in range(len(SortedFList)):
                    if(SortedFList[i]['feasible']==True):
                        vIndex=SortedFList[i]['vIndex']
                        rIndex=SortedFList[i]['Position']
                        DC.VehicleList[vIndex].routing.insert(rIndex,CustomerCopy[customer])
                        feasible=True
                        break
                if(feasible==False):
                    DC.addVehicle(self.__VehicleList[0][0],self.__VehicleList[0][1],self.__VehicleList[0][2],self.__VehicleList[0][3])
                    DC.VehicleList[DC.GetNumberVehicles()-1].routing.append(CustomerCopy[customer])
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
        DCID=self.__DCList[dcIndex].getID()            
        totalDistanceTraveled=self.__DistanceMatrix[DCID][vehicle.routing[0].getID()]
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
        TotalCost1=candidate1.getTotalCost()
        TotalCost2=candidate2.getTotalCost()
        if(TotalCost1<TotalCost2):
            return 0
        else: 
            return 1
        return
    def __CurrentBest(self):
        min=1000000
        index=0
        for popIndex in range(len(self.__population)):
            TotalCost=0
            for DCIndex in range(len(self.__DCList)):
                TotalCost+=self.__population[popIndex].DC[DCIndex].getTotalCost()
            if(TotalCost<min):
                min=TotalCost
                index=popIndex
        return min,index
    def Max(self):        
        MaxValue=0
        MaxIndex=0
        for i in range(len(self.__population)):
            TotalCost=self.__population[i].getTotalCost()
            #print("Total cost of population {0}: {1}".format(i,TotalCost))
            if(TotalCost>MaxValue):
                MaxValue=TotalCost
                MaxIndex=i
                #print("Max cost: {0}".format(MaxValue))
        return MaxIndex
    #check constraint functions
    def checkCondition(self,Rweight,Rvolume,Vehicle):
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
                for vehicle in range(self.__population[num].DC[DCIndex].GetNumberVehicles()):
                    for customer in range(self.__population[num].DC[DCIndex].VehicleList[vehicle].getNumberofRoutes()):
                        print("vehicle {0}: {1}".format(
                            vehicle,self.__population[num].DC[DCIndex].VehicleList[vehicle].routing[customer].getID()))
                    print("total distance travelled: {0}".format(
                        self.__population[num].DC[DCIndex].VehicleList[vehicle].getTotalDistanceTravelled()))
                print("Total cost: {0}".format(self.__population[num].DC[DCIndex].getTotalCost()))
            print("total cost of population: {0}".format(self.__population[num].getTotalCost()))
        print("")
        for num in range(len(self.__children)):
            print("child {0}".format(num))
            for DCIndex in range(len(self.__DCList)):
                print("Distribution Center {0}".format(DCIndex))
                for vehicle in range(self.__children[num].DC[DCIndex].GetNumberVehicles()):
                    for customer in range(self.__children[num].DC[DCIndex].VehicleList[vehicle].getNumberofRoutes()):
                        print("vehicle {0}: {1}".format(
                            vehicle,self.__children[num].DC[DCIndex].VehicleList[vehicle].routing[customer].getID()))
                    print("total distance travelled: {0}".format(
                    self.__children[num].DC[DCIndex].VehicleList[vehicle].getTotalDistanceTravelled()))
                print("Total cost: {0}".format(self.__children[num].DC[DCIndex].getTotalCost()))
            print("total cost of children: {0}".format(self.__children[num].getTotalCost()))
        return
    def BestSolutionDisplay(self):
        for DCIndex in range(len(self.__DCList)):
            print("Distribution Center {0}".format(DCIndex))
            for vehicle in range(self.__bestSolution['route'].DC[DCIndex].GetNumberVehicles()):
                for customer in range(self.__bestSolution['route'].DC[DCIndex].VehicleList[vehicle].getNumberofRoutes()):
                    print("vehicle {0}: {1}".format(
                        vehicle,self.__bestSolution['route'].DC[DCIndex].VehicleList[vehicle].routing[customer].getID()))
                print("total distance travelled: {0}".format(
                    self.__bestSolution['route'].DC[DCIndex].VehicleList[vehicle].getTotalDistanceTravelled()))
            print("Total cost: {0}".format(self.__bestSolution['route'].DC[DCIndex].getTotalCost()))
        print("total cost of best solution: {0}".format(self.__bestSolution['route'].getTotalCost()))
    #main loop function
    def mainloop(self,maxIter,CThold):
        count=0
        for i in range(maxIter):
            parent1=self.Selection(0.8)
            parent2=self.Selection(0.8)
            while(parent1==parent2):
                parent2=self.Selection(0.8)
            #crossover
            rand=random.uniform(0,1)
            if(rand<=CThold):                
                self.crossover(parent1,parent2)
                for ChildIndex in range(len(self.__children)):
                    TotalCustomer=0
                    for DCIndex in range(len(self.__DCList)):
                        for vIndex in range(self.__children[ChildIndex].DC[DCIndex].GetNumberVehicles()):
                            TotalCustomer+=self.__children[ChildIndex].DC[DCIndex].VehicleList[vIndex].getNumberofRoutes()
                    print("Total Customer of child {0}: {1}".format(ChildIndex,TotalCustomer))
            else:
                self.__children=[]
                self.__children.append(copy.deepcopy(self.__population[parent1]))
                self.__children.append(copy.deepcopy(self.__population[parent2]))
            #mutation
            rand=random.uniform(0,1)
            if(rand>CThold):
                popIndex=random.randrange(0,len(self.__population))
                if(self.Mutation(self.__population[popIndex])==False):
                    del self.__population[popIndex]
                    rParent=random.randrange(0,len(self.__population))
                    self.__population.append(copy.deepcopy(self.__population[rParent]))
            rand=random.uniform(0,1)
            if(len(self.__children)>0):
                if(rand>CThold):
                    popIndex=random.randrange(0,len(self.__children))
                    if(self.Mutation(self.__children[popIndex])==False):
                        del self.__children[popIndex]
            #Survivor selection       
            self.SurvivorSelection()
            self.deleteChildren()
            print("_________________________")
            CurrentBest,index=self.__CurrentBest()
            if(CurrentBest<self.__bestSolution['Value']):
                self.__bestSolution['Value']=CurrentBest
                self.__bestSolution['route']=copy.deepcopy(self.__population[index])
                count=0
            print("current best solution: {0}, individual {1}".format(CurrentBest,index))
            print("best solution: {0}".format(self.__bestSolution['Value']))
            #self.BestSolutionDisplay()
            print(i)
            count+=1
            if(count==50):
                print("best solution obtained!")
                self.BestSolutionDisplay()
                return 0
            
