import sys
from end_conditions import Condition
from heuristic import Algorithm
from Candidate import Candidate
def main():
    no_arguments=len(sys.argv)

    if no_arguments != 2:
        print('Proper execution: python script <file_configuration.txt>')
    else:
        conf_file=sys.argv[1]
        initial_solution=Candidate(conf_file,None)
        algorithm=Algorithm(init_solution=initial_solution,end_condition=Condition.WITHOUT_BETTER_SOLUTION,p_cross=0.2,p_mutation=0.3,no_candidates=5,starting_population=10) 
        algorithm.run()
        algorithm.display_results()

if __name__=="__main__":
    main()