from nltk.corpus import wordnet as wn
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

pronoun_list = ["people", "anybody", "anyone", "everybody", "everyone","somebody",
"someone", "something", "she", "he", "him", "her", "you", "I",
"we", "us", "they", "them", "it"]


def yes_no_answer (q_sent, a_sent):
    token_q = nlp.word_tokenize(q_sent)
    token_a = nlp.word_tokenize(a_sent)
    dep_q = nlp.dependency_parse(q_sent)
    dep_a = nlp.dependency_parse(a_sent)
    match = [u'ROOT', u'nsubj', u'dobj']
    for a in dep_a:
        if a[0] in match:
            part = a[0]
            a_word = token_a[a[2]-1]
            # if pronoun, check for exact pronoun match
            # todo: implement hierarchy/logic, functionality for "it" references
            if a_word in pronoun_list:
                for q in dep_q:
                    if q[0] == a[0]:
                        q_word = token_q[q[2]-1]
                        if q_word != a_word:
                            #print ("PRONOUN: FALSE")
                            return "No"
                        else:
                            print("PRONOUN: TRUE")
            else:
               a_synset = wn.synsets(token_a[a[2]-1])
               for q in dep_q:
                   if q[0] == a[0]:
                       q_synset = wn.synsets(token_q[q[2]-1])
                       qa_dict = sim_dict(q_synset, a_synset)
                       print ("SYNSETS", a_synset, q_synset)
                       print ("DICT", qa_dict)
                       if True not in qa_dict.values():
                           return "No"
    return "Yes"

yes_no_answer("Do penguins eat food?", "Birds eat food.")
yes_no_answer("Does the penguin give food?", "Birds provide nutrients.")
yes_no_answer("Do humans ride vehicles?", "The man drives airplanes.")
yes_no_answer("Does it eat food?", "it eats food.")
