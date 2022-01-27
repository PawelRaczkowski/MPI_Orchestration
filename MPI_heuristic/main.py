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
    list1=[3,5,7]
    value=list1[1]
    list1[1]=list1[2]
    list1[2]=value

    #main()