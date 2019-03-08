import Simulated_Annealing
import cities
SA=Simulated_Annealing.Simmulated_Annealing()
city_list=cities.cities_list()
#add cities' location
city_list.add_city(1,1)
city_list.add_city(3,1)
city_list.add_city(3,2)
city_list.add_city(5,5)
city_list.add_city(15,5)
#intializate components
city_list.shuffle_path()
city_list.display_cityinfo()
SA.set_temp(1000)
SA.set_current(city_list.calc_newSolution())
SA.display_info()
#start SA
neighbour=0.0
rate=0.1
while SA.get_temp()>1:    
    neighbour=city_list.calc_newSolution()
    if SA.calculate(neighbour,rate) == True:
        SA.set_current(neighbour)
    if SA.get_current()<SA.get_best():
        city_list.display_cityinfo()
        SA.set_best(SA.get_current())
    city_list.shuffle_path()
SA.display_info()
city_list.plot_location()


