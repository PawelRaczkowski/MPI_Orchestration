import sys
from end_conditions import Condition
from heuristic import Algorithm
from Candidate import Candidate
def test_function(initial_solution):
    print("calculate cost for minizinc solution: ")
    candidate=Candidate("", initial_solution)
    candidate.content_on_server[0]=[ True, False, False,  True, False]
    candidate.content_on_server[1]= [False, False, False, False, False]
    candidate.content_on_server[2] = [False, False, False, False, False]
    candidate.content_on_server[3]= [False,  True, False, False,  True]
    candidate.content_on_server[4]= [False, False, True, False, False]
    candidate.assign_content_to_user(initial_solution)
    candidate.calculate_total_cost(initial_solution)
    print('Total cost: ', candidate.total_cost)

def main():
    no_arguments=len(sys.argv)
    
    if no_arguments != 2:
        print('Proper execution: python script <file_configuration.txt>')
    else:
        print("START PROGRAM")
        conf_file=sys.argv[1]
        print("CREATING INITIAL SOLUTION...")
        initial_solution=Candidate(conf_file,None)
        print("CREATING ALGORITHM")
        #test_function(initial_solution)
        algorithm=Algorithm(init_solution=initial_solution,end_condition=Condition.WITHOUT_BETTER_SOLUTION,p_cross=0.2,p_mutation=0.3,no_candidates=5,starting_population=10) 
        print("RUN ALGORITHM...")       
        algorithm.run()
        print("*****DISPLAYING FINISH RESULT****")
        algorithm.display_results()

if __name__=="__main__":
    main()