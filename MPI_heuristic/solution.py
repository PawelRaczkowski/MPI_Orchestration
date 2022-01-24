from cmath import sqrt

from location import Location
class Solution():
    def __init__(self,conf_file) -> None:
        self.no_servers=0
        self.no_users=0
        self.no_contents=0

        self.servers_locations=[]
        self.users_locations=[]
        self.content_sizes=[]

        self.capacities=[]
        self.matrix_interest=[]
        self.parse_file(conf_file)
        
        self.distances_orch_servers=[]
        self.distances_user_servers=[]
        self.content_on_server=[]

        self.use_server=[]
        
        for i in range(self.no_users):
            self.use_server.append([])
            for j in range(self.no_contents):
                self.use_server[i].append([])
                for k in range(self.no_servers):
                    self.use_server[i,j].append(False)

        for i in range(self.no_servers):
            x1=self.servers_locations[i].get_x()
            y1=self.servers_locations[i].get_y()
            self.distances_orch_servers.append(self.calculate_distance(x1,0,y1,0))

            for u in range(self.no_users):
                x2=self.users_locations[u].get_x()
                y2=self.users_locations[u].get_y()
                self.distances_user_servers.append([])
                self.distances_user_servers.append(self.calculate_distance(x1,x2,y1,y2))

            self.content_on_server.append([])
            for j in range(self.no_contents):
                self.content_on_server[i].append(False)
        
        




    def parse_file(self,conf_file):
        f=open(conf_file, "r")

        self.no_servers=int(f.readline(),16) ## number of objects
        self.no_users=int(f.readline(),16)
        self.no_contents=int(f.readline(),16)

        f.readline()

        for i in range(self.no_servers):
            line=f.readline().split(' ') # SERVER LOCATIONS
            x=line[0]
            y=line[1]
            location=Location(x,y)
            self.servers_locations.append(location)

            capacity=int(f.readline(),16) ## CAPACITIES
            self.capacities.append(capacity)

        f.readline()

        for i in range(self.no_users):
            line=f.readline().split(' ') # user locations
            x=line[0]
            y=line[1]
            location=Location(x,y)
            self.users_locations.append(location)

            self.matrix_interest.append([]) # matrix of interest

            line=f.readline().split(' ')
            for j in range(len(line)):
                self.matrix_interest[i].append(int(line[j],16))

        
        f.readline()

        for i in range(self.no_contents): # size of contents
            size=int(f.readline(),16)
            self.content_sizes.append(size)

    def calculate_distance(self,x1,x2,y1,y2):
        return sqrt(pow(x1-x2,2)+pow(y1-y2,2))

    def calculate_allocation_cost(self):
        cost=0
        for i in range(self.no_servers):
            for j in range(self.no_contents):
                if self.content_on_server[i,j]:
                    cost+=self.distances_orch_servers[i]*self.content_sizes[j]
        return cost
    def calculate_users_cost(self):
        cost=0
        for i in range(self.no_servers):
            for j in range(self.no_contents):
                for u in range(self.no_users):
                    if self.use_server[u,j,i]:
                        cost+=5.0
        return cost
    def calculate_load_cost(self):
        cost=0
        for i in range(self.no_servers):
            for j in range(self.no_contents):
                for u in range(self.no_users):
                    if self.use_server[u,j,i]:
                        cost+=self.content_sizes[j]*self.distances_user_servers[u,i]
        return cost

    def calculate_total_cost(self):
        C_allocation=self.calculate_allocation_cost()
        C_users=self.calculate_users_cost()
        C_load_server=self.calculate_load_cost()
        return C_allocation+C_users+C_load_server


    def display_results(self):
        for i in range(self.no_servers):
            for j in range(self.no_contents):
                print("For server nr {}, content type nr {} -> {}".format(i+1,j+1,self.content_on_server[i,j]))