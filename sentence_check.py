from nltk.corpus import wordnet as wn
from nltk.tree import ParentedTree
import requests
import json
from collections import defaultdict

from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://corenlp.run', port=80)
# nlp = StanfordCoreNLP(r'/Users/cynthiachen/Documents/2018/MIT_final/stanford-corenlp-full-2018-02-27')

# tests if two words for similar by hypernym hyponym or synset
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

def are_antonyms (q_lem, a_lem):
    # EXAMPLE are_antonyms(wn.lemmas("slowly"), wn.lemmas("quickly"))
    for q in q_lem:
        for a in a_lem:
            if q in a.antonyms():
                return True
    return False

# extracts either the NP or the VP of the sentence
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

# given the ParentedTree of a parse, create a flattened VP dictinoary
def create_tree_dict (tree, top_key):
    tree_dict = defaultdict(list)
    for i in tree:
        tree_dict[i.label()].append(i)
    if top_key in tree_dict: # gets rid of nested VP
        for key in tree_dict.keys():
            if key in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']: # we don't care about modals
                tree_dict.pop(key)
        for j in tree_dict[top_key]: # bring nested VP out
            for k in j:
                tree_dict[k.label()].append(k)
        tree_dict.pop(top_key)
    for key in tree_dict.keys(): # rename all verb forms into 'Verb'
        if key in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
            tree_dict['Verb'].extend(tree_dict.pop(key))
    return tree_dict

def compare_verbs (q_verb, a_verb):
    print "---VERBS---", q_verb, a_verb, q_verb[0][0], a_verb[0][0]
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
            q_syn = wn.synsets(q.leaves()[0]) # extract interested adverb
            a_syn = wn.synsets(a.leaves()[0])
            sim = sim_dict(q_syn, a_syn) # should adverbs we compared with sim_dict?
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
            if (q[0] == a[0]): # only comparing similar PP
                print q[0], a[0]
                pp_comparison.append(noun_check(flatten_noun(q[1]), flatten_noun(a[1]))) # call noun_check
            else:
                pp_comparison.append(False)
    return (any(v == True for v in pp_comparison))

def compare_do(q_do, a_do):
    print "---DO---", q_do, a_do
    if (not q_do or not a_do):
        return True
    return noun_check(flatten_noun(q_do[0]), flatten_noun(q_do[0])) # call noun_check for direct object

# general check for verb phrases
def verb_check (qtree, atree):
    dict_q = create_tree_dict(qtree, 'VP')
    dict_a = create_tree_dict(atree, 'VP')
    return ((compare_verbs(dict_q['Verb'], dict_a['Verb']) == compare_neg(dict_q['RB'], dict_a['RB']))
    and compare_do(dict_q['NP'], dict_a['NP'])
    and compare_adv(dict_q['ADVP'], dict_a['ADVP'])
    and compare_pp(dict_q['PP'], dict_a['PP']))
    # return compareVerbs and compareNeg and compareAdv and compareDO and comparePP and compareSBAR

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

def noun_check (qdict, adict):
    #compareNouns
    print (qdict, adict)
    if "Noun" in qdict and "Noun" in adict:
         nn_sims = sim_dict(wn.synsets(qdict["Noun"][0][0]), wn.synsets(adict["Noun"][0][0]))
         print("Noun", any(v for v in nn_sims.values()))
         if not (any(v for v in nn_sims.values())):
             return False
    if "DT" in qdict and "DT" in adict:
        #every some no
        q_dt = qdict["DT"][0][0].lower()
        a_dt = adict["DT"][0][0].lower()
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
    return True


def compare_sentences(sent1, sent2):
    v1 = get_tree_part(sent1, 'VP')
    v2 = get_tree_part(sent2, 'VP')
    verb_sim = verb_check(v1, v2)
    print ("VERB SIMILARITY", verb_sim)
    n1 = get_tree_part(sent1, 'NP')
    n2 = get_tree_part(sent2, 'NP')
    noun_sim = noun_check(flatten_noun(n1), flatten_noun(n2))
    print ("NOUN SIMILARITY", noun_sim)
    return verb_sim and noun_sim

print compare_sentences("Do some penguins read books about swimming daily?", "Every animal in the northern hemisphere reads books about exercising daily.")

nlp.close() # Do not forget to close! The backend server will consume a lot memery.

# Moving Forward
# - Cynthia: SBAR, test set - verb
# - Sherry: clean up your shit, SBAR, test set - noun, try catch
# - Future: antonyms, update, possible amendmends (if then, is it true/false, conjugations)

# Examples to fix
# DOUBLE NEGATIVE - > print compare_sentences("Do no penguins run on the ice?", "Every penguin does not run quickly on the ice.")

# Things to ask
# StanfordCoreNLP (parsing, and the server)
# scope? double negatives, conjunctions
