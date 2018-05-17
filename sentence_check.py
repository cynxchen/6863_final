from nltk.corpus import wordnet as wn
from nltk.tree import ParentedTree
import requests
import json
import pprint
from collections import defaultdict

from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://corenlp.run', port=80)
print_switch = False
# nlp = StanfordCoreNLP(r'/Users/cynthiachen/Documents/2018/MIT_final/stanford-corenlp-full-2018-02-27')

def change_print (print_arg):
    global print_switch
    print_switch = bool(print_arg)

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

def are_antonyms (q_syns, a_syns):
    # EXAMPLE are_antonyms(wn.synsets("slowly"), wn.synsets("quickly"))
    for q_syn in q_syns:
        for a_syn in a_syns:
            q_lems = q_syn.lemmas()
            a_lems = a_syn.lemmas()
            for q in q_lems:
                for a in a_lems:
                    if q in a.antonyms():
                        return True
    return False

# extracts either the NP or the VP of the sentence
def get_tree_part (sentence, part):
    url = "http://corenlp.run:80/tregex"
    request_paramsN = {"pattern": "(NP[$VP]>S)|(NP[$VP]>S\\n)|(NP\\n[$VP]>S)|(NP\\n[$VP]>S\\n)|(NP[$VP]>SQ)"}
    request_paramsV = {"pattern": "(VP[$NP]>S)|(VP[$NP]>S\\n)|(VP\\n[$NP]>S)|(VP\\n[$NP]>S\\n)|(VP[$NP]>SQ)"}
    select = request_paramsN if part == "NP" else request_paramsV
    try:
        request = requests.post(url, data=sentence, params=select)
        json = request.json()
        if print_switch: print (json)
    except:
        print("Cannot connect to coreNLP server. Try again later.")
        raise ConnectionError
        return
    try:
        string = str(dict(json['sentences'][0])['0']['match'])
        tree = ParentedTree.fromstring(string)
        return tree
    except:
        print("Parsing issue in sentence:", sentence)
        print("Recieved parse:", nlp.parse(sentence))
        raise ValueError
        return

# given the ParentedTree of a parse, create a flattened VP dictinoary
def flatten_verb (tree, top_key):
    tree_dict = defaultdict(list)
    for i in tree:
        tree_dict[i.label()].append(i)
    if top_key in tree_dict: # gets rid of nested VP
        for key in list(tree_dict):
            if key in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']: # we don't care about modals
                tree_dict.pop(key)
        for j in tree_dict[top_key]: # bring nested VP out
            for k in j:
                tree_dict[k.label()].append(k)
        tree_dict.pop(top_key)
    for key in list(tree_dict): # rename all verb forms into 'Verb'
        if key in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
            tree_dict['Verb'].extend(tree_dict.pop(key))
    return tree_dict

def compare_verbs (q_verb, a_verb):
    if print_switch: print ("---VERBS---", q_verb, a_verb, q_verb[0][0], a_verb[0][0])
    q_syn = wn.synsets(q_verb[0][0]) # extract interested verb
    a_syn = wn.synsets(a_verb[0][0])
    sim = sim_dict(q_syn, a_syn)
    return any(v == True for v in sim.values())

def compare_neg (q_rb, a_rb):
    if print_switch: print ("---NEG---", q_rb, a_rb)
    if (not q_rb and not a_rb): # neither negated
        return True
    elif (not q_rb or not a_rb): # one of them negated
        return False
    elif (((q_rb[0][0] in ['not', "n't"]) and (a_rb[0][0] in ['not', "n't"]))): # both negated
        return True
    elif (((q_rb[0][0] in ['not', "n't"]) or (a_rb[0][0] in ['not', "n't"]))):
        return False
    else: # other weird cases
        return True

def compare_adv(q_adv, a_adv):
    if print_switch: print ("---ADV---", q_adv, a_adv)
    if (not q_adv or not a_adv): # checks to see if we have any adverbs to compare
        return True
    adv_comparison = []
    for q in q_adv:
        for a in a_adv:
            # if print_switch: print (q, a)
            q_syns = wn.synsets(q.leaves()[0]) # extract interested verb
            a_syns = wn.synsets(a.leaves()[0])
            if (are_antonyms(q_syns, a_syns)):
                return False
    return True

def compare_pp(q_pp, a_pp):
    if print_switch: print ("---PP---", q_pp, a_pp)
    if ((not q_pp) or (not a_pp)): # checks to see if we have any adverbs to compare
        return True
    pp_comparison = []
    for q in q_pp:
        for a in a_pp:
            # if print_switch: print (q, a)
            if (q[0] == a[0]):
                # if print_switch: print (q[0], a[0])
                # if print_switch: print ("--noun-check-in-pp--", q[1], a[1])
                pp_comparison.append(noun_check(q[1], a[1]))
            # else:
            #     pp_comparison.append(False)
    return (not pp_comparison or any(v == True for v in pp_comparison))

def compare_do(q_do, a_do):
    if print_switch: print ("---DO---", q_do, a_do)
    if (not q_do or not a_do):
        return True
    return noun_check(q_do[0], a_do[0]) # call noun_check for direct object

def compare_adj(q_adjs, a_adjs):
    if print_switch: print ("---ADJ---", q_adjs, a_adjs)
    if q_adjs and a_adjs:
        for q_jj in q_adjs:
            for a_jj in a_adjs:
                # if print_switch: print(q_jj[0],a_jj[0])
                if (are_antonyms(wn.synsets(q_jj[0]), wn.synsets(a_jj[0]))):
                    return False
    return True

def compare_adjp(q_adjp, a_adjp, q_adj, a_adj):
    if print_switch: print ("---ADJP---", q_adjp, a_adjp)
    if ((not q_adjp and not q_adj) or (not a_adjp and not a_adj)): # checks to see if we have any adverbs to compare
        return True
    comparison = {}
    if (q_adj and a_adj) or (q_adjp and a_adjp):
        for q in (q_adj or q_adjp[0]):
            for a in (a_adj or a_adjp[0]):
                if (q.label() == a.label() == "JJ"):
                    comparison['JJ'] = compare_adj([q],[a])
                    # if print_switch: print("JJ", compare_adj([q], [a]))
                elif (q.label() == a.label() == "RB"):
                    if (not compare_neg([q],[a])):
                        comparison['RB'] = False
                        # if print_switch: print("NEG", False)
                    else:
                        comparison['RB'] = compare_adj([q],[a])
                        # if print_switch: print("RB", compare_adj([q], [a]))
    else:
        for q in (q_adj or q_adjp[0]):
            for a in (a_adj or a_adjp[0]):
                if (q.label() == a.label() == "JJ"):
                    comparison['JJ'] = compare_adj([q],[a])
                    # if print_switch: print("JJ", compare_adj([q], [a]))
                elif (q.label() == "RB" or a.label() == "RB"):
                    if (not compare_neg([q],[a])):
                        comparison['RB'] = False
                        # if print_switch: print("NEG", False)
                    else:
                        comparison['RB'] = compare_adj([q],[a])
                        # if print_switch: print("RB", compare_adj([q], [a]))
    # if print_switch: print (comparison.values())
    return all(v for v in comparison.values())

# general check for verb phrases
def verb_check (qtree, atree):
    dict_q = flatten_verb(qtree, 'VP')
    dict_a = flatten_verb(atree, 'VP')
    return ((compare_verbs(dict_q['Verb'], dict_a['Verb']) == compare_neg(dict_q['RB'], dict_a['RB']))
    and compare_do(dict_q['NP'], dict_a['NP'])
    and compare_adv(dict_q['ADVP'], dict_a['ADVP'])
    and compare_pp(dict_q['PP'], dict_a['PP'])
    and compare_adjp(dict_q['ADJP'], dict_a['ADJP'], dict_q['JJ'], dict_a['JJ']))
    # return compareVerbs and compareNeg and compareAdv and compareDO and comparePP and compareSBAR

def flatten_noun (tree):
    flat = defaultdict(list)
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
                if subpart.label() in ["NN", "NNS", "NNP", "NNPS", "PRP"]:
                    flat["Noun"] = [subpart]
                elif subpart.label() in flat:
                    flat[subpart.label()].append(subpart)
                else:
                    flat[subpart.label()] = [subpart]
    flatten_n_rec(tree)
    return flat

def compare_nouns(q_noun, a_noun):
    if print_switch: print ("---NOUN---", q_noun, a_noun)
    if q_noun and a_noun:
         nn_sims = sim_dict(wn.synsets(q_noun[0][0]), wn.synsets(a_noun[0][0]))
         return (any(v for v in nn_sims.values()))
    print("Sentence may not have a subject")

def compare_dt(q_dts, a_dts):
    if print_switch: print ("---DET---", q_dts, a_dts)
    #every some no
    if q_dts and a_dts:
        q_dt = q_dts[0][0].lower()
        a_dt = a_dts[0][0].lower()
        if q_dt == "every" or q_dt == "all":
            if not (a_dt == "every" or a_dt == "all"):
                return False
        elif q_dt == "some":
            if not (a_dt != "no"):
                return False
        elif q_dt == "no":
            if not (a_dt == "no"):
                return False
        elif a_dt == "no":
            return False
    return True

def noun_check (qtree, atree):
    #compareNouns
    dict_q = flatten_noun(qtree)
    dict_a = flatten_noun(atree)
    return (compare_nouns(dict_q['Noun'], dict_a['Noun'])
    and compare_dt(dict_q['DT'], dict_a['DT'])
    and compare_pp(dict_q['PP'], dict_a['PP'])
    and compare_adjp(dict_q['ADJP'], dict_a['ADJP'], dict_q['JJ'], dict_a['JJ']))


def compare_sentences(sent1, sent2, print_arg=False):
    change_print(print_arg)
    try:
        n1 = get_tree_part(sent1, 'NP')
        v1 = get_tree_part(sent1, 'VP')
        n2 = get_tree_part(sent2, 'NP')
        v2 = get_tree_part(sent2, 'VP')
    except ValueError as e:
        return "Error."
    except ConnectionError as e:
        return "Error."

    verb_sim = verb_check(v1, v2)
    if print_switch: print ("VERB SIMILARITY", verb_sim)

    noun_sim = noun_check(n1, n2)
    if print_switch: print ("NOUN SIMILARITY", noun_sim)
    return "Yes." if verb_sim and noun_sim else "No."

nlp.close() # Do not forget to close! The backend server will consume a lot memery.
