from nltk.corpus import wordnet as wn
from nltk.tree import Tree, ParentedTree
import pprint

from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://corenlp.run', port=80)

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

# STUFF FOR TREGEX
import requests
import json
#
url = "http://corenlp.run:80/tregex"

request_paramsN = {"pattern": "(NP[$VP]>S)|(NP[$VP]>S\\n)|(NP\\n[$VP]>S)|(NP\\n[$VP]>S\\n)|(NP[$VP]>SQ)"}
request_paramsV = {"pattern": "(VP[$NP]>S)|(VP[$NP]>S\\n)|(VP\\n[$NP]>S)|(VP\\n[$NP]>S\\n)|(VP[$NP]>SQ)"}

def get_Reg_Tree(sentence, pattern):
    reqN = requests.post(url, data=sentence, params=pattern)
    treeN_test = str(dict((reqN.json())['sentences'][0])['0']['match'])
    return ParentedTree.fromstring(treeN_test)

q_sent = "Does some yellow dog climb up?"
a_sent = "Some red animal climbs."

q_N = get_Reg_Tree(q_sent, request_paramsN)
a_N = get_Reg_Tree(a_sent, request_paramsN)

print(q_N)
print(a_N)

def flatten_noun (tree):
    flat = {}
    def flatten_n_rec(tree):
        if any(sub.label() == 'NP' for sub in tree):
            for subpart in tree:
                if subpart.label() == 'NP':
                    flatten_n_rec(subpart)
                elif subpart.label() in flat:
                    flat[subpart.label()].append(subpart)
                else:
                    flat[subpart.label()] = [subpart]
        elif tree != None:
            for subpart in tree:
                if subpart.label() in ["NN", "NNS", "NNP", "NNPS"]:
                    flat["Noun"] = [subpart]
                elif subpart.label() in flat:
                    flat[subpart.label()].append(subpart)
                else:
                    flat[subpart.label()] = [subpart]
    flatten_n_rec(tree)
    return flat
    #print(flat)

q_posdict = flatten_noun(q_N)
a_posdict = flatten_noun(a_N)

def noun_check (qdict, adict):
    #compareNouns
    if "Noun" in qdict and "Noun" in adict:
         nn_sims = sim_dict(wn.synsets(qdict["Noun"][0][0]), wn.synsets(adict["Noun"][0][0]))
         print("Noun", any(v for v in nn_sims.values()))
         if not (any(v for v in nn_sims.values())):
             return False
    if "DT" in qdict and "DT" in adict:
        #every some no
        q_dt = qdict["DT"][0][0]
        a_dt = adict["DT"][0][0]
        print(q_dt)

        if q_dt.lower() == "every":
            print("DT", q_dt, a_dt, (a_dt == "every"))
            if not (a_dt == "every"):
                return False
        elif q_dt.lower() == "some":
            print("DT", q_dt, a_dt, (a_dt != "no"))
            if not (a_dt != "no"):
                return False
        elif q_dt.lower() == "no":
            print("DT", q_dt, a_dt, (a_dt == "no"))
            if not (a_dt == "no"):
                return False
    if "JJ" in qdict and "JJ" in adict:
        q_jjlist = qdict["JJ"]
        a_jjlist = adict["JJ"]
        for q_jj in q_jjlist:
            for a_jj in a_jjlist:
                jj_sims = sim_dict(wn.synsets(q_jj[0]), wn.synsets(a_jj[0]))
                print("Adj", any(v for v in jj_sims.values()))
                if not (any(v for v in jj_sims.values())):
                    return False
    if "PP" in qdict and "PP" in adict:
        q_pplist = qdict["PP"]
        a_pplist = adict["PP"]
        for q_pp in q_pplist:
            for a_pp in a_pplist:
                print(q_pp, a_pp)
                if q_pp[0] == a_pp[0]:
                    ppcheck = noun_check(flatten_noun(q_pp[1]), flatten_noun(a_pp[1]))
                    print("PP", q_pp[1], a_pp[1])
                    if not ppcheck:
                        return False

    #compareNouns and compareDT and compareJJ and comparePP and compareSBAR

noun_check (q_posdict, a_posdict)


nlp.close() # Do not forget to close! The backend server will consume a lot memery.
