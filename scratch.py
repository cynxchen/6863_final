from nltk.corpus import wordnet as wn
from nltk.tree import Tree, ParentedTree
import logging

# word = wn.synsets('run')
# for w in word:
#     print w.hypernyms()

from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://corenlp.run', port=80,quiet=False, logging_level=logging.DEBUG)
# nlp = StanfordCoreNLP(r'/Users/cynthiachen/Documents/2018/MIT_final/stanford-corenlp-full-2018-02-27')

# sent = 'Penguins eat fish.'
# s = nlp.parse(sent)
# help(nlp.tregex)
# print nlp.tregex(sentence = "Penguins eat fish",pattern = "S < VP=target")

# question = 'Do penguins eat food?'
# tokenq = nlp.word_tokenize(question)
# posq =  nlp.pos_tag(question)
# nameq = nlp.ner(question)
# treeq = nlp.parse(question)
# depq = nlp.dependency_parse(question)
#
# answer = 'Birds eat food'
# token = nlp.word_tokenize(answer)
# pos = nlp.pos_tag(answer)
# name = nlp.ner(answer)
# tree =  nlp.parse(answer)
# dep = nlp.dependency_parse(answer)

class POS(object):
    def __init__(self, label, q, a):
        self.label = label
        self.q = q
        self.a = a
        self.modifiers = []

    def add_modifier(self, obj):
        self.modifiers.append(obj)

    def create_sim_dict(self):
        return sim_dict(wn.synsets(self.q), wn.synsets(self.a))

    def similar(self):
        curr_lvl = True if self.q == self.a else any(v == True for v in self.create_sim_dict().values())
        return curr_lvl and all(m.similar() == True for m in self.modifiers)

noun = POS("NNS", "penguin", "penguin")
noun.similar()
adj = POS("NNP", "red", "blue")
adj.similar()
noun.add_modifier(adj)
noun.similar()
sim_dict(wn.synsets("will sleep"), wn.synsets("sleep"))

def sim_dict (q_synset, a_synset):
    sim = {"hypernym": False,
            "hyponym": False,
            "synset": False}
    for q in q_synset:
        for a in a_synset:
            if not sim["hypernym"] and a in q.hypernym_paths()[0]:
                sim["hypernym"]=True
            if not sim["hyponym"] and q in a.hypernym_paths()[0]:
                sim["hyponym"]=True
            if not sim["synset"] and q == a:
                sim["synset"]=True
    return sim

# def yes_no_answer (q_sent, a_sent):
#     token_q = nlp.word_tokenize(q_sent)
#     token_a = nlp.word_tokenize(a_sent)
#     dep_q = nlp.dependency_parse(q_sent)
#     dep_a = nlp.dependency_parse(a_sent)
#     POS_dict = {}
#     for q in dep_q:
#         for a in dep_a:
#             if q[0] == a[0]:
#                 POS_dict = POS(token_q[q[2]-1],token_a[a[2]-1])
#                 if
    # match = [u'ROOT', u'nsubj', u'dobj']
    # for a in dep_a:
    #     if a[0] in match:
    #         part = a[0]
    #         a_synset = wn.synsets(token_a[a[2]-1])
    #         for q in dep_q:
    #             if q[0] == a[0]:
    #                 q_synset = wn.synsets(token_q[q[2]-1])
    #                 qa_dict = sim_dict(q_synset, a_synset)
    #                 # print "SYNSETS", a_synset, q_synset
    #                 print a[0], qa_dict
    #                 if True not in qa_dict.values():
    #                     return "No"
    # return "Yes"

# yes_no_answer("Do penguins eat food?", "Birds eat food.")
# yes_no_answer("Does the penguin give food?", "Birds provide nutrients.")
# yes_no_answer("Do humans ride vehicles?", "The man drives airplanes.")
# yes_no_answer("Do penguins eat clouds?", "Penguins eat shrimp.")
#
# nlp.dependency_parse("Does the department that sell knives also sell blade sharpeners?")
# nlp.dependency_parse("No departments sell knives.")
# nlp.dependency_parse("Does the department that sell knives also sell blade sharpeners?")
# nlp.dependency_parse("No departments sell knives.")
#
# nlp.dependency_parse("Do red penguins eat fish?")
# t = nlp.parse("Blue penguins eat fish.")
# t2 = nlp.parse("Red penguins eat fish.")
# parsetree = Tree.fromstring(str(t))
# ptree = ParentedTree.fromstring(str(t))
# ptree2 = ParentedTree.fromstring(str(t2))
# print ptree.leaves()
# ptree.pprint()
# print ptree[0][0][0].label()

def create_tree(label, ptree, ptree2):
    if (type(ptree[0]) == str):
        # print ptree[0], ptree2[0]
        return POS(label, ptree[0], ptree2[0])
    else:
        obj1 = POS(label, "", "")
        for i in ptree:
            for j in ptree2:
                if (i.label() == j.label()):
                    # print i.label(), j.label()
                    obj1.add_modifier(create_tree(i.label(), i, j))
        return obj1

def print_tree (obj):
    for i in obj.modifiers:
        print i.label, i.q, i.a, i.similar()
        print_tree(i)

def compare_sentences(sent1, sent2):
    t1 = nlp.parse(sent1)
    t2 = nlp.parse(sent2)
    ptree1 = ParentedTree.fromstring(str(t1))
    ptree2 = ParentedTree.fromstring(str(t2))
    POS_obj = create_tree('ROOT', ptree1, ptree2)
    print_tree(POS_obj)
    return POS_obj.similar()

test = create_tree('ROOT', ptree, ptree2)
test.similar()
print_tree(test)
compare_sentences("Blue penguins eat fish.", "Red penguins eat fish.")

compare_sentences("All penguins will definitely sleep.", "All penguins will absolutely sleep.")
print nlp.parse("While they are red, Pusheen walked on the grass.")
print nlp.parse("The red penguin flew fast")
# drive sucks
nlp.close()
for i in ptree.subtrees():
    print i
# STUFF FOR TREGEX
import requests
import json
#
url = "http://corenlp.run:80/tregex"
request_params = {"pattern": "(NP[$VP]>S)|(NP[$VP]>S\\n)|(NP\\n[$VP]>S)|(NP\\n[$VP]>S\\n)|(NP[$VP]>SQ)"}
# request_params = {"pattern": "(VP[$NP]>S)|(VP[$NP]>S\\n)|(VP\\n[$NP]>S)|(VP\\n[$NP]>S\\n)|(VP[$NP]>SQ)"}
r = requests.post(url, data='The red penguins from Anarctica sleep?', params=request_params)
json_data = r.json()
tree_test = str(dict(json_data['sentences'][0])['0']['match'])
tree_tree = ParentedTree.fromstring(tree_test)

r2 = requests.post(url, data='The penguin cries', params=request_params)
json_data2 = r2.json()
print json_data2
tree_test2 = str(dict(json_data2['sentences'][0])['0']['match'])
tree_tree2 = ParentedTree.fromstring(tree_test2)

print tree_tree2
print tree_tree

def Noun_Check (qtree, atree):
    if any(sub.label() == 'NP' for sub in qtree):
        flatten
    if any(sub.label() == 'NP' for sub in atree):
        flatten
    compareNouns and compareDT and compareJJ and comparePP and compareSBAR

print tree_tree[0].label()

#
# nlp.close() # Do not forget to close! The backend server will consume a lot memery.
