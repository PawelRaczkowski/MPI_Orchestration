from xmlrpc.client import MAXINT
from Candidate import Candidate
from end_conditions import Condition
from random import randrange
import random
import time
import copy

class Algorithm():
    LIMIT_GENERATIONS=100
    LIMIT_TIME=1000 # in seconds
    LIMIT_LACK_BETTER_SOLUTION=100

    def __init__(self,init_solution,end_condition,p_cross,p_mutation,no_candidates) -> None:
        self.initial_solution=init_solution # initial solution to kandydat referencyjny gdzie są wgrane dane z pliku
        # każdy inny ma modyfikowane tylko zmienne decyzyjne czyli use_server oraz contents_on_server
        self.cost=MAXINT # ostateczny koszt obliczony-najlepszy
        self.end_condition=end_condition#końcowy warunek zakończenia
        self.probability_cross=p_cross#pstwo krzyżowania
        self.probability_mutation=p_mutation#pstwo mutacji
        self.no_candidates=no_candidates #liczba kandydatów na każdą generacje

        self.candidates=self.generate_candidates()# generacja początkowej generacji

        self.time_of_execution=0
        self.no_generations=0
        self.no_lack_better=0

    def run(self):
        start=time.time()
        while self.check_end_condition():
            self.mutate()
            self.cross()
            self.get_best_candidates()
            self.check_new_solution()
            self.time_of_execution=time.time()-start

    def mutate(self):
        for k in range(len(self.candidates)):
            for i in range(self.initial_solution.no_servers):
                if random.uniform(0,1) < self.probability_mutation:
                    candidate=copy.deepcopy(self.candidates[k])
                    index_one=randrange(self.initial_solution.no_contents)
                    index_two=index_one
                    while index_two == index_one:
                        index_two=randrange(self.initial_solution.no_contents)
                    candidate.content_on_server[i][index_one]= not self.candidates[k].content_on_server[i][index_one]
                    candidate.content_on_server[i][index_two]= not self.candidates[k].content_on_server[i][index_two]
                    if self.check_limits(candidate):
                        self.candidates.append(candidate)
                        self.candidates[-1].calculate_total_cost()
                    else:
                        i-=1



    def check_limits(self,candidate): # sprawdza czy nie przeciążony każdy z serwerów
        for i in range(candidate.no_servers):
            if sum(candidate.content_on_server[i]) > self.initial_solution.capacities[i]:
                return False
        return True

    def cross(self):
        self.shuffle()
        no_results=len(self.candidates)//2
        for i in range(no_results):
            if(random.uniform(0,1) <self.probability_cross):
                candidate=self.cross_genes(self.candidates[2*i],self.candidates[2*i+1])
                if self.check_limits(candidate):
                    self.candidates.append()
                else:
                    i-=1 #aby iteracja nie poszła na marne

    def cross_genes(self,one,two):
        candidate=copy.deepcopy(one)
        for i in range(self.initial_solution.no_servers):
            if randrange(0,2) ==1 : # 50% szans
                candidate.content_on_server[i]=copy.deepcopy(two[i])
                candidate.calculate_total_cost()
        return candidate


    def shuffle(self):
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
        no_users=self.initial_solution.no_users

        initial_use_server=copy.deepcopy(self.initial_solution.use_server)
        initial_contents_on_server=copy.deepcopy(self.initial_solution.content_on_server)

        for i in range(no_servers):
            for j in range(no_contents):
                index_content=randrange(no_contents)
                index_user=randrange(no_users)
                initial_contents_on_server[i][index_content]= not initial_contents_on_server[i][index_content]
                initial_use_server[index_user][index_content][i]= not initial_use_server[index_user][index_content][i]
                candidate=Candidate("")
                candidate.assign_solution(initial_contents_on_server,initial_use_server)
                if self.check_limits(candidate):
                    candidate.calculate_total_cost()
                    candidates.append(candidate)
                else:
                    j-=1
                
        return candidates

    def get_best_candidates(self):
        self.candidates.sort(key=lambda x: x.total_cost, reverse=False)
        self.candidates=self.candidates[:self.no_candidates]
        self.no_generations+=1

    def check_new_solution(self):
        if self.candidates[0].total_cost <= self.cost:
            self.cost=self.candidates[0].total_cost
            self.no_lack_better=0
        else:
            self.no_lack_better+=1
    def check_end_condition(self):
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