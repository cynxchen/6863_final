from sentence_check import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("sentences", type=str, help="Question and Answer Pair", nargs=2)
parser.add_argument("-p", action='store_true', help="trees and component comparison verbose printing")
args = parser.parse_args()

print compare_sentences(args.sentences[0], args.sentences[1], print_arg=args.p)

#cmd
