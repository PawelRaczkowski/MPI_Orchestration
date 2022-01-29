from xmlrpc.client import MAXINT
from Candidate import Candidate
from end_conditions import Condition
from random import randrange
import random
import time
import copy

class Algorithm():
    LIMIT_GENERATIONS=100
    LIMIT_TIME=10 # in seconds
    LIMIT_LACK_BETTER_SOLUTION=20

    def __init__(self,init_solution,end_condition,p_cross,p_mutation,no_candidates,starting_population) -> None:
        self.initial_solution=init_solution # initial solution to kandydat referencyjny gdzie są wgrane dane z pliku
        # każdy inny ma modyfikowane tylko zmienne decyzyjne czyli use_server oraz contents_on_server
        self.cost=MAXINT # ostateczny koszt obliczony-najlepszy
        self.end_condition=end_condition#końcowy warunek zakończenia
        self.probability_cross=p_cross#pstwo krzyżowania
        self.probability_mutation=p_mutation#pstwo mutacji
        self.no_candidates=no_candidates #liczba kandydatów na każdą generacje
        self.starting_population=starting_population
        self.candidates=self.generate_candidates()# generacja początkowej generacji

     

        self.time_of_execution=0
        self.no_generations=0
        self.no_lack_better=0

    def run(self):
        start=time.time()
        #print("STARTOWA POPULACJA.... ")
        #self.display_candidates()
        while self.check_end_condition():
            #print("MUTATION...")
            self.mutate()
            #print("CROSSING...")
            self.cross()
            #print("FILTERING BEST CANDIDATES...")
            self.get_best_candidates()
            #print("****** DISPLAY OF CANDIDATES ******")
            #self.display_candidates()
            #print("CHECKING NEW SOLUTION...")
            self.check_new_solution()

            self.time_of_execution=time.time()-start

    def display_candidates(self):
        for cand in self.candidates:
            cand.display_results(self.initial_solution)

    def mutate(self):
        k=0
        max_k=len(self.candidates)-1
        while k != max_k: 
            candidate=copy.deepcopy(self.candidates[k])
            for i in range(self.initial_solution.no_servers):
                if random.uniform(0,1) < self.probability_mutation:
                    if_mutation=True
                    index_one=randrange(self.initial_solution.no_contents)
                    index_two=index_one
                    while index_two == index_one:
                        index_two=randrange(self.initial_solution.no_contents)
                    temp=candidate.content_on_server[i][index_one]
                    candidate.content_on_server[i][index_one]= candidate.content_on_server[i][index_two]
                    candidate.content_on_server[i][index_two]= temp
                    
            candidate.assign_content_to_user(self.initial_solution)
            candidate.calculate_total_cost(self.initial_solution)
            if self.check_limits(candidate,self.initial_solution):
                #print("Generated candidate after mutation....")
                #candidate.display_results(self.initial_solution)
                self.candidates.append(candidate)
            k+=1




    def check_limits(self,candidate,initial_solution): # sprawdza czy nie przeciążony każdy z serwerów
        
        for i in range(initial_solution.no_servers):
            sum_overload=0
            for j in range(initial_solution.no_contents):
                if candidate.content_on_server[i][j]:
                    sum_overload+=initial_solution.content_sizes[j]
            if sum_overload > self.initial_solution.capacities[i]:
                #print("too much...")
                return False
        return True

    def cross(self):
        self.shuffle()
        no_results=len(self.candidates)//2
        i=0
        while i != no_results:
            if(random.uniform(0,1) <self.probability_cross):
                candidate=self.cross_genes(self.candidates[2*i],self.candidates[2*i+1])
                if self.check_limits(candidate,self.initial_solution): #nie można przekroczyć pojemności serwerów
                    i+=1
                    #print("Generated candidate after crossing....")
                    #candidate.display_results(self.initial_solution)
                    self.candidates.append(candidate)


    def cross_genes(self,one,two):
        candidate=copy.deepcopy(one)
        for i in range(self.initial_solution.no_servers):
            if randrange(0,2) ==1 : # 50% szans
                candidate.content_on_server[i]=copy.deepcopy(two.content_on_server[i])
        candidate.assign_content_to_user(self.initial_solution)
        candidate.calculate_total_cost(self.initial_solution)        
        return candidate


    def shuffle(self): #zmiana kolejności kandydatów
        n=len(self.candidates) 
        while n>1:
            n-=1
            k=randrange(n+1)
            value=copy.deepcopy(self.candidates[k])
            self.candidates[k]=copy.deepcopy(self.candidates[n])
            self.candidates[n]=copy.deepcopy(value) 

    def generate_candidates(self):
        candidates=[]
        no_servers=self.initial_solution.no_servers
        no_contents=self.initial_solution.no_contents

        
        k=0
        while k != self.starting_population:
            initial_contents_on_server=copy.deepcopy(self.initial_solution.content_on_server)
            for i in range(no_servers):
                for j in range(no_contents//2):
                    index_content=randrange(no_contents)
                    initial_contents_on_server[i][index_content]= not self.initial_solution.content_on_server[i][index_content]
            candidate=Candidate("",self.initial_solution)
            candidate.assign_solution(initial_contents_on_server)
            if self.check_limits(candidate,self.initial_solution):
                candidate.assign_content_to_user(self.initial_solution)
                candidate.calculate_total_cost(self.initial_solution)
                k+=1
                candidates.append(candidate)
          
        return candidates

    def get_best_candidates(self):
        self.candidates.sort(key=lambda x: x.total_cost, reverse=False)
        self.candidates=copy.deepcopy(self.candidates[:self.no_candidates])
        self.no_generations+=1

    def check_new_solution(self):
        if self.candidates[0].total_cost <= self.cost:
            self.cost=self.candidates[0].total_cost
            self.no_lack_better=0
        else:
            self.no_lack_better+=1
    def check_end_condition(self):
        #print("CHECKING CONDITION...")
        if self.end_condition==Condition.TIME:
            if self.time_of_execution < self.LIMIT_TIME:
                return True
        elif self.end_condition==Condition.WITHOUT_BETTER_SOLUTION:
            if self.no_lack_better < self.LIMIT_LACK_BETTER_SOLUTION:
                return True
        else:
            if self.no_generations < self.LIMIT_GENERATIONS:
                return True
        return False

    def display_results(self):
        self.candidates[0].display_results(self.initial_solution)
        print('No generations: {}'.format(self.no_generations))