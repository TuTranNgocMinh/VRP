import numpy as np
from random import randint
from random import betavariate
class kmeans():
    """cluster addresses using K means clustering algorithm"""
    def __init__(self, customer_list,vehicle_list,n_clusters,tolerance,max_iter):
        self.__cust_list=customer_list
        self.__vehicle_list=vehicle_list
        self.__k_clusters=n_clusters
        self.clustered_data=0
        self.__tolerance=tolerance
        self.__max_iter=max_iter
        return
    def __euclidean_distance(self,current,centroids):
        """calculate euclidean distance between current cluster list and centroid of each cluster """
        return np.sqrt(np.power((centroids["lat"] - current['lat']), 2)+np.power((centroids['lng'] - current['lng']), 2))
    def __avg(self):
        """calculate mean of each cluster in cluster list"""
        avg=[]
        for i in range(len(self.clustered_data)):
            lat=0
            lng=0
            for j in range(len(self.clustered_data[i])):
                lat=lat+self.clustered_data[i][j].location.coordinates['lat']
                lng=lng+self.clustered_data[i][j].location.coordinates['lng']
            lat=lat/len(self.clustered_data[i])
            lng=lng/len(self.clustered_data[i])
            avg.append({'lat':lat,'lng':lng})
        return avg
    def __set_centroid(self,iter):
        """if iter=1,initiate centroids.Else, choose new centroid from each current cluster"""
        if iter==1:
            self.centroid_list=[]
            for i in range(self.__k_clusters):
                index=randint(0,len(self.__cust_list)-1)
                self.centroid_list.append(self.__cust_list[index].location.coordinates)
        if iter>1:
            avg=self.__avg()
            for i in range(len(avg)):
                self.centroid_list[i]=avg[i] 
        return
    def __isdifference(self,current_centroids):
        """check for changes between current and new clusters, return false if the difference < tolerence"""
        for i in range(len(self.centroid_list)):
            diff_x=np.abs(current_centroids[i]['lat']-self.centroid_list[i]['lat'])
            diff_y=np.abs(current_centroids[i]['lng']-self.centroid_list[i]['lng'])
            print("{0}, {1}".format(diff_x,diff_y))
            if (diff_x>self.__tolerance)or(diff_y>self.__tolerance):
                return True
        return False
    def fit(self):
        """cluster data using kmeans """
        iter=1
        self.__set_centroid(iter)        
        while (iter<=self.__max_iter):
            self.clustered_data=[[] for i in range(self.__k_clusters)] #initiate list of clustered data
            current_centroids=self.centroid_list.copy()
            for i in range(len(self.__cust_list)):
                temp_list=[] #initiate temporary list for comparision
                for centroid in range(self.__k_clusters):
                    temp_list.append(self.__euclidean_distance(self.__cust_list[i].location.coordinates,self.centroid_list[centroid]))
                min=np.argmin(temp_list) #determine centroid which closest to the point
                self.clustered_data[min].append(self.__cust_list[i])
            for i in range(len(self.centroid_list)):
                if len(self.clustered_data[i])==0:
                    print("cluster {0} is empty. assign a random location from customer list".format(i))
                    index=randint(0,len(self.__cust_list)-1)
                    self.clustered_data[i].append(self.__cust_list[index])
            iter=iter+1
            self.__set_centroid(iter)
            if not(self.__isdifference(current_centroids)):
                print("data convergence, exit")
                return
        return
    def check_condition(self):
        for i in range(len(self.clustered_data)):
            weight=0
            volume=0
            routing=[]
            for j in range(len(self.clustered_data[i])):
                weight+=self.clustered_data[i][j].weight
                volume+=self.clustered_data[i][j].volume
                routing.append(self.clustered_data[i][j].location.coordinates)
            #print("weight = {0}".format(weight))
            #print("volume = {0}".format(volume))
            for vehicle in range(len(self.__vehicle_list)):
                if (self.__vehicle_list[vehicle].weight>weight)and(self.__vehicle_list[vehicle].volume>(volume*90/100)):
                    if not(self.__vehicle_list[vehicle].routing):
                        self.__vehicle_list[vehicle].routing=routing.copy()
                        break
class coordinates():
    """coordinate class"""
    def __init__(self,x_coord,y_coord):
        self.x=x_coord
        self.y=y_coord
        return

