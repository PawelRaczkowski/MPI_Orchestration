import sys
from heuristic import Algorithm
from Candidate import Candidate
def main():
    no_arguments=len(sys.argv)

    if no_arguments != 2:
        print('Proper execution: python script <file_configuration.txt>')
    else:
        conf_file=sys.argv[1]
        initial_solution=Candidate(conf_file)
        algorithm=Algorithm(initial_solution)
        algorithm.run()

if __name__=="__main__":
    main()