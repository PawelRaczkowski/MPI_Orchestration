import sys
from heuristic import Algorithm
def main():
    no_arguments=len(sys.argv)

    if no_arguments != 2:
        print('Proper execution: python script <file_configuration.txt>')
    else:
        conf_file=sys.argv[1]
        algorithm=Algorithm(conf_file)
        algorithm.content_distribution()
        algorithm.display_results()

if __name__=="__main__":
    main()