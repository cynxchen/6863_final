from nltk.corpus import wordnet as wn
from nltk.tree import Tree, ParentedTree

from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://corenlp.run', port=80)
# nlp = StanfordCoreNLP(r'/Users/cynthiachen/Documents/2018/MIT_final/stanford-corenlp-full-2018-02-27')

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

# TESTING POS CLASS
# noun = POS("NNS", "penguin", "penguin")
# noun.similar()
# adj = POS("NNP", "red", "blue")
# adj.similar()
# noun.add_modifier(adj)
# noun.similar()
# sim_dict(wn.synsets("definite"), wn.synsets("absolute"))

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

t = nlp.parse("Blue penguins eat fish.")
t2 = nlp.parse("Red penguins eat fish.")
ptree = ParentedTree.fromstring(str(t))
ptree2 = ParentedTree.fromstring(str(t2))
test = create_tree('ROOT', ptree, ptree2)
test.similar()
print_tree(test)

compare_sentences("Blue penguins eat fish in Antartica.", "Red penguins eat fish.")
compare_sentences("All penguins will run.", "All penguins will move.")

nlp.close()
