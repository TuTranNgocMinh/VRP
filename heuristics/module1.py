import pandas
import location
import customer
from vehicle import vehicle,VehicleList
from random import randint
import numpy as np
import DataNoGmap as Dt
from model import model_GA
def test2():
    loc=[]
    origins=[]
    list=pandas.read_csv("data30.csv",encoding='utf-8-sig')
    DC=[location.location("10 Ly Tu Trong,quan 1,Ho Chi Minh"),location.location("10 Le Van Viet, quan 9, ho chi minh"),location.location("30 Phu Tho Hoa, quan Tan Phu, Ho Chi Minh")]
    for i in range(len(list.index)):
        print(i)
        loc.append(customer.customer(i,list['name'][i],list['size'][i],list['weight'][i],list['quantity'][i],list['address'][i]))
        origins.append(loc[i].getLocation())
    #add DC
    origins.append(DC[0].coordinates)
    origins.append(DC[1].coordinates)
    origins.append(DC[2].coordinates)
    mat=location.dist_matrix(origins,origins)
    mat.get_approxdistance()
    dist_matrix=mat.getDistance()
    print(dist_matrix)
    df=pandas.DataFrame(dist_matrix)
    writer = pandas.ExcelWriter('C:/Users/Tu Tran Ngoc Minh/Desktop/heuristics/Distance_30_2.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    return
def VRP():
    DC=location.location("100 Truong chinh, Tan Binh, Ho Chi Minh")
    cust=[]
    origins=[DC.coordinates]
    list=pandas.read_csv("test.csv")
    for i in range(len(list['name'])):
        cust.append(customer.customer(list['name'][i],list['Qty'][i],list['size'][i],list['weight'][i],list['destination'][i],list['deadline'][i]))
        origins.append(cust[i].location.coordinates)
        cust[i].display()
    print(origins)
    mat=location.dist_matrix(origins,origins)
    #mat.get_realdistance()
    mat.get_approxdistance()
    print(" ")
    mat.display()
    vehicle_list=[vehicle.vehicle("truck",volume=10000,weight=5000),vehicle.vehicle("truck",volume=2000,weight=800),
                  vehicle.vehicle("truck",volume=10000,weight=5000),vehicle.vehicle("truck",volume=7500,weight=2000),
                  vehicle.vehicle("truck",volume=2000,weight=800),vehicle.vehicle("truck",volume=5000,weight=1200)]
    kmeans=VRPmodel.kmeans(cust,vehicle_list,2,0.0001,1000)
    kmeans.fit()
    for i in range(len(kmeans.clustered_data)):
        print("centroid {0}".format(i))
        print(kmeans.clustered_data[i])
    kmeans.check_condition()
    for i in range(len(vehicle_list)):
        if (vehicle_list[i].routing):
            print("vehicle {0} with volume = {1}, weight = {2} is assigned: {3}".format(i,vehicle_list[i].volume, vehicle_list[i].weight,vehicle_list[i].routing))    
    return
def test_kmeans():
    cust=[]
    for i in range(30):
        x = randint(1,50)
        y=randint(1,50)
        cust.append({'lat':x,'lng':y})
    kmeans=VRPmodel.kmeans(cust,[],2,0.001,1000)
    kmeans.fit()
    print("centroid list: {0}".format(kmeans.centroid_list))  
    for i in range(len(kmeans.clustered_data)):
        print("centroid {0}".format(i))
        print(kmeans.clustered_data[i])
def testGA():
    DCLocation=[{'lng': 106.6559861, 'lat': 10.7976518}, {'lng': 106.777597, 'lat': 10.799542}]   
    CustomerLocList=[{'lng': 106.677597, 'lat': 10.799542}, {'lng': 106.657301, 'lat': 10.771048}, 
                 {'lng': 106.695201, 'lat': 10.7801688}, {'lng': 106.702432, 'lat': 10.7887654}, 
                 {'lng': 106.719758, 'lat': 10.799096}, {'lng': 106.653311, 'lat': 10.776861}, 
                 {'lng': 106.6296637, 'lat': 10.7883491}, {'lng': 106.7753504, 'lat': 10.8478509}, 
                 {'lng': 106.7561567, 'lat': 10.851093}]
    CustomerData=pandas.read_csv("test.csv",encoding='utf-8-sig')
    #create customer list
    CustomerList=[]
    for i in range(len(CustomerLocList)):
        CustomerList.append(
            Dt.CustomerNoGmap(i,CustomerData['name'][i],CustomerData['Qty'][i],
                              CustomerData['size'][i],CustomerData['weight'][i],CustomerLocList[i]))
    del CustomerData
    #create DC List
    DCList=[]
    DCList.append(Dt.DCNoGmap(DCLocation[0],len(CustomerList)))
    DCList.append(Dt.DCNoGmap(DCLocation[1],len(CustomerList)+1))
    #print("ID DC 0: {0}".format(DCList[0].getID()))
    #print("ID DC 1: {0}".format(DCList[1].getID()))
    #create Origins list
    OriginsList=CustomerLocList[:]
    OriginsList.append(DCLocation[0])
    OriginsList.append(DCLocation[1])
    #create Distance and Time Matrix
    Distance=Dt.DistMatrixNoGmap(OriginsList,OriginsList)
    Distance.get_approxdistance()
    #create Vehicle List[Name,Volume,Weight,number of vehicles]
    VehicleList=[["truck",50000,3000,10]]
    #create model GA
    GA=model_GA(CustomerList,VehicleList,Distance,DCList,0.8,0.2)
    print("")
    LocGroup=GA.initGroup()
    print(LocGroup)
    for i in range(len(LocGroup)):
        print("")
        for j in range(len(LocGroup[i])):
            print(LocGroup[i][j].getLocation())
    GA.initpopulation(7,LocGroup)
    GA.mainloop(10,0.8)
    bestSolution=GA.getBestSolution()
    print(bestSolution)
test2()