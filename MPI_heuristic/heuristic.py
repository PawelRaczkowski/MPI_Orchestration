from xmlrpc.client import MAXINT
class Algorithm():
    def __init__(self,initial_solution,end_condition,p_cross,p_mutation,no_candidates) -> None:
        self.initial_solution=initial_solution
        self.cost=MAXINT
        self.end_condition=end_condition
        self.probability_cross=p_cross
        self.probability_mutation=p_mutation
        self.no_candidates=no_candidates


    def run(self):
        while self.check_end_condition():
            pass
        pass
    def mutate(self):
        pass
    def cross(self):
        pass
    
    def check_end_condition(self):
        pass