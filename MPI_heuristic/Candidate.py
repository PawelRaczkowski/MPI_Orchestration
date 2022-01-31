from cmath import sqrt
import copy
from xmlrpc.client import MAXINT
import math
from location import Location
import re
class Candidate():
    def __init__(self,conf_file,initial_solution) -> None:
        self.no_servers=0
        self.no_users=0
        self.no_contents=0

        self.servers_locations=[]
        self.users_locations=[]
        self.content_sizes=[]

        self.capacities=[]
        self.matrix_interest=[]
        if conf_file != "": # jest jeden kandydat który ma dane zczytane z pliku, reszta polega tylko na content_on_server
            self.parse_file(conf_file)
        
        self.distances_orch_servers=[]
        self.distances_user_servers=[]


        self.content_on_server=[]
        self.use_server=[]
        if initial_solution is not None:
            self.content_on_server=copy.deepcopy(initial_solution.content_on_server)
            self.use_server=copy.deepcopy(initial_solution.use_server)

        self.total_cost=MAXINT # cost of solution

        for i in range(self.no_users):
            self.use_server.append([])
            for j in range(self.no_contents):
                self.use_server[i].append([])
                for k in range(self.no_servers):
                    self.use_server[i][j].append(False)

        for i in range(self.no_servers):
            x1=self.servers_locations[i].get_x()
            y1=self.servers_locations[i].get_y()
            self.distances_orch_servers.append(self.calculate_distance(x1,0,y1,0))
            self.distances_user_servers.append([]) # distances_user_server[i,j] odległość usera j do serwera i
            for u in range(self.no_users):
                x2=self.users_locations[u].get_x()
                y2=self.users_locations[u].get_y()
                self.distances_user_servers[-1].append(self.calculate_distance(x1,x2,y1,y2))

            self.content_on_server.append([])
            for j in range(self.no_contents):
                self.content_on_server[i].append(False) # content_on_server[i][j] na serwerze i jest treść j
        


    def assign_solution(self, content_on_server):
        self.content_on_server=copy.deepcopy(content_on_server)

    def parse_file(self,conf_file):
        f=open(conf_file, "r")

        self.no_servers=int(f.readline()) ## number of objects
        self.no_users=int(f.readline())
        self.no_contents=int(f.readline())
        f.readline()

        for i in range(self.no_servers):
            line=f.readline().split(' ') # SERVER LOCATIONS
            x=int(line[0])
            y=int(line[1])
            location=Location(x,y)
            self.servers_locations.append(location)

            capacity=int(f.readline()) ## CAPACITIES
            self.capacities.append(capacity)

        f.readline()

        for i in range(self.no_users):
            line=f.readline().split(' ') # user locations
            x=int(line[0])
            y=int(line[1])
            location=Location(x,y)
            self.users_locations.append(location)

            self.matrix_interest.append([]) # matrix of interest

            line=f.readline().split(' ')
            
            for j in range(len(line)):
                self.matrix_interest[i].append(self.str2bool(line[j]))
            
        f.readline()
        line=f.readline().split(' ')
        for j in range(len(line)):
            self.content_sizes.append(int(line[j]))
    def str2bool(self, v):
        return v.lower() in ["True", "true", "true\n"]

    def calculate_distance(self,x1,x2,y1,y2):
        return math.sqrt((x1-x2)**2+(y1-y2)**2)

    def calculate_lack_of_demand_matrix(self,initial_solution,flag):
        cost=0
        for u in range(initial_solution.no_users):
            for j in range(initial_solution.no_contents):
                if initial_solution.matrix_interest[u][j]:
                    if initial_solution.matrix_interest[u][j] not in self.use_server[u][j]:
                        cost+=100000.0
        return cost
    def calculate_allocation_cost(self,initial_solution):
        cost=0
        for i in range(initial_solution.no_servers):
            for j in range(initial_solution.no_contents):
                if self.content_on_server[i][j]:
                    cost+=initial_solution.distances_orch_servers[i]*initial_solution.content_sizes[j]
        return cost
    def calculate_users_cost(self,initial_solution):
        cost=0
        for i in range(initial_solution.no_servers):
            for j in range(initial_solution.no_contents):
                for u in range(initial_solution.no_users):
                    if self.use_server[u][j][i]:
                        cost+=5.0
        return cost
    def calculate_load_cost(self,initial_solution):
        cost=0
        for i in range(initial_solution.no_servers):
            for j in range(initial_solution.no_contents):
                for u in range(initial_solution.no_users):
                    if self.use_server[u][j][i]:
                        cost+=initial_solution.content_sizes[j]*initial_solution.distances_user_servers[u][i]
        return cost

    def calculate_total_cost(self,initial_solution):
        C_allocation=self.calculate_allocation_cost(initial_solution)
        C_users=self.calculate_users_cost(initial_solution)
        C_load_server=self.calculate_load_cost(initial_solution)
        C_lack_matrix=self.calculate_lack_of_demand_matrix(initial_solution,flag=False)

        self.total_cost=C_allocation+C_users+C_load_server+C_lack_matrix


    def display_results(self,initial_solution):
        print("Cost of solution-> {}".format(self.total_cost))
        for i in range(initial_solution.no_servers):
            print("For server nr {}:".format(i+1))
            for j in range(initial_solution.no_contents):
                 print("content type nr {} -> {}".format(j+1,self.content_on_server[i][j]))
    
    def assign_content_to_user(self,initial_solution):
        for u in range(initial_solution.no_users):
            for c in range(initial_solution.no_contents):
                if initial_solution.matrix_interest[u][c]:
                    server_to_assign=self.assign_server(u,c,initial_solution)
                    if server_to_assign!=-1:
                        self.use_server[u][c][server_to_assign]=True
                    else:
                        for i in range(initial_solution.no_servers):
                            self.use_server[u][c][i]=False
                else:
                    for i in range(initial_solution.no_servers):
                        self.use_server[u][c][i]=False


    def assign_server(self,user,content,initial_solution):
        distance=MAXINT
        server=-1
        for i in range(initial_solution.no_servers):
            if self.content_on_server[i][content]:
                if initial_solution.distances_user_servers[i][user] <= distance:
                    distance=initial_solution.distances_user_servers[i][user]
                    server=i
        return server