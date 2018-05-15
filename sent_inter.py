from sentence_check import *
import argparse
from six.moves import input

def compare(args):
    while (True):
        question = str(input());
        if (question in ['', 'exit', 'quit']): break
        answer = str(input());
        if (answer in ['', 'exit', 'quit']): break
        print (compare_sentences(question, answer, print_arg=args.p))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument("sentences", type=str, help="Question and Answer Pair", nargs=2)
    parser.add_argument("-p", action='store_true', help="trees and component comparison verbose printing")
    args = parser.parse_args()
    compare(args)

#cmd
