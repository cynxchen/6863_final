# Translating Indirect Responses to Direct Answers
Cynthia Chen (cchen16), Sherry Xu (sherryxu), Adis Ojeda (adiso)

### Overview
Our final project for 6.863J is on researching conversations and understanding how indirect responses to Yes-No questions can be translated into a direct "Yes" or "No" answer.

Our system attempts to translate indirect to direct answers through parsing Question and Answer (QA) pairs to identify key components and then comparing each component with WordNet and other techniques.

This repository contains 4 files.

### Setup
To run our program, you will need to have the python wrapper for StanfordCoreNLP installed on your device.
```
pip install stanfordcorenlp
```
Here is the python wrapper we use: https://github.com/Lynten/stanford-corenlp
### Description of Files
#### 1. sentence_check.py
This file contains our system.

#### 2. sent_term.py
This file is a wrapper for our project that allows the user to test QA pairs through terminal arguments.
```
python sent_term.py question indirect-answer [-h] [-p]
```
optional arguments:
*  -h, --help  show this help message and exit
*  -p          trees and component comparison verbose printing

#### 3. sent_inter.py
_\*\*\* we suggest using this to test our project._

This file is a wrapper for our project that allows the user to test QA pairs through interactive prompting.
```
python sent_inter.py [-h] [-p]
```
optional arguments:
*  -h, --help  show this help message and exit
*  -p          trees and component comparison verbose printing

#### 4. testing.py
This file contains test set of 35 QA pairs in addition to some working example sentences. Running this file will run tests on the test set.
```
python testing.py
```
### Additional Notes
If you receive the error ```Cannot connect to coreNLP server. Try again later.``` then that signifies that StanfordCoreNLP's server is not connecting and may be down. Try waiting a couple minutes before reattempting. This problem is outside the scope of our project and is not due to issues with our system.

If you receive the error ```Parsing issue in sentence: ...``` then that means StanfordCoreNLP's parser returned an incorrect parse or a parse that our system cannot handle.

### Built With
* WordNet: https://wordnet.princeton.edu/
* NLTK: https://www.nltk.org/
* StanfordCoreNLP: https://stanfordnlp.github.io/CoreNLP/
