from nltk.corpus import wordnet as wn
from nltk.tree import ParentedTree
import requests
import json
from collections import defaultdict

from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://corenlp.run', port=80)
# nlp = StanfordCoreNLP(r'/Users/cynthiachen/Documents/2018/MIT_final/stanford-corenlp-full-2018-02-27')

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

def get_tree_part (sentence, part):
    url = "http://corenlp.run:80/tregex"
    request_paramsN = {"pattern": "(NP[$VP]>S)|(NP[$VP]>S\\n)|(NP\\n[$VP]>S)|(NP\\n[$VP]>S\\n)|(NP[$VP]>SQ)"}
    request_paramsV = {"pattern": "(VP[$NP]>S)|(VP[$NP]>S\\n)|(VP\\n[$NP]>S)|(VP\\n[$NP]>S\\n)|(VP[$NP]>SQ)"}
    select = request_paramsN if part == "NP" else request_paramsV
    request = requests.post(url, data=sentence, params=select)
    json = request.json()
    print json
    string = str(dict(json['sentences'][0])['0']['match'])
    tree = ParentedTree.fromstring(string)
    return tree

def create_tree_dict (tree, top_key):
    tree_dict = defaultdict(list)
    for i in tree:
        tree_dict[i.label()].append(i)
    if top_key in tree_dict:
        for j in tree_dict[top_key]:
            for k in j:
                tree_dict[k.label()].append(k)
        tree_dict.pop(top_key)
    for key in tree_dict.keys():
        if key in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
            tree_dict['Verb'].extend(tree_dict.pop(key))
    return tree_dict

def compare_verbs (q_verb, a_verb):
    print "---VERBS---", q_verb, a_verb
    q_syn = wn.synsets(q_verb[0][0]) # extract interested verb
    a_syn = wn.synsets(a_verb[0][0])
    sim = sim_dict(q_syn, a_syn)
    return any(v == True for v in sim.values())

def compare_neg (q_rb, a_rb):
    print "---NEG---", q_rb, a_rb
    if (not q_rb and not a_rb): # neither negated
        return True
    elif (not q_rb or not a_rb): # one of them negated
        return False
    elif (((q_rb[0][0] in ['not', "n't"]) and (a_rb[0][0] in ['not', "n't"]))): # both negated
        return True
    else: # other weird cases
        return False

def compare_adv(q_adv, a_adv):
    print "---ADV---", q_adv, a_adv
    if (not q_adv or not a_adv): # checks to see if we have any adverbs to compare
        return True
    adv_comparison = []
    for q in q_adv:
        for a in a_adv:
            print q, a
            q_syn = wn.synsets(q.leaves()[0]) # extract interested verb
            a_syn = wn.synsets(a.leaves()[0])
            sim = sim_dict(q_syn, a_syn)
            adv_comparison.append(any(v == True for v in sim.values()))
    return (any(v == True for v in adv_comparison))

def compare_pp(q_pp, a_pp):
    print "---PP---", q_pp, a_pp
    if (not q_pp or not a_pp): # checks to see if we have any adverbs to compare
        return True
    pp_comparison = []
    for q in q_pp:
        for a in a_pp:
            print q, a
            if (q[0] == a[0]):
                print q[0], a[0]
                # noun_check(q[1], a[1])
                q_syn = wn.synsets(q.leaves()[-1]) # extract interested verb
                a_syn = wn.synsets(a.leaves()[-1])
                sim = sim_dict(q_syn, a_syn)
                print sim
                pp_comparison.append(any(v == True for v in sim.values()))
            else:
                pp_comparison.append(False)
    return (any(v == True for v in pp_comparison))

def verb_check (qtree, atree):
    dict_q = create_tree_dict(qtree, 'VP')
    dict_a = create_tree_dict(atree, 'VP')
    return ((compare_verbs(dict_q['Verb'], dict_a['Verb']) == compare_neg(dict_q['RB'], dict_a['RB']))
    and compare_adv(dict_q['ADVP'], dict_a['ADVP']) and compare_pp(dict_q['PP'], dict_a['PP']))
    # return compareVerbs and compareNeg and compareAdv and compareDO and comparePP and compareSBAR

def compare_sentences(sent1, sent2):
    v1 = get_tree_part(sent1, 'VP')
    v2 = get_tree_part(sent2, 'VP')
    verb_sim = verb_check(v1, v2)
    return verb_sim

print compare_sentences("Have the bears tried the food?", "The bears tested the food")

nlp.close() # Do not forget to close! The backend server will consume a lot memery.
