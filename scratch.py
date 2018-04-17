from nltk.corpus import wordnet as wn

word = wn.synsets('run')
for w in word:
    print w.hypernyms()

from stanfordcorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://corenlp.run', port=80)

question = 'Who ran the race?'
# print 'Tokenize:', nlp.word_tokenize(question)
# print 'Part of Speech:', nlp.pos_tag(question)
# print 'Named Entities:', nlp.ner(question)
print 'Constituency Parsing:', nlp.parse(question)
# print 'Dependency Parsing:', nlp.dependency_parse(question)

answer = 'Jane raced'
# print 'Tokenize:', nlp.word_tokenize(answer)
# print 'Part of Speech:', nlp.pos_tag(answer)
# print 'Named Entities:', nlp.ner(answer)
print 'Constituency Parsing:', nlp.parse(answer)
# print 'Dependency Parsing:', nlp.dependency_parse(answer)

import requests

url = "http://corenlp.run:80/tregex"
request_params = {"pattern": "(NP[$VP]>S)|(NP[$VP]>S\\n)|(NP\\n[$VP]>S)|(NP\\n[$VP]>S\\n)"}
r = requests.post(url, data=answer, params=request_params)
print r.json()

nlp.close() # Do not forget to close! The backend server will consume a lot memery.
