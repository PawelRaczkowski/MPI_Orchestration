import sys
from heuristic import Algorithm
from solution import Solution
def main():
    no_arguments=len(sys.argv)

    if no_arguments != 2:
        print('Proper execution: python script <file_configuration.txt>')
    else:
        conf_file=sys.argv[1]
        initial_solution=Solution(conf_file)
        algorithm=Algorithm(initial_solution)

        algorithm.run()

if __name__=="__main__":
    main()