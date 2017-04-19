from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
from nltk import tree
import nltk
import sys
import codecs

def read_file( filename ):
    f = codecs.open(filename,encoding='utf-8', mode='r')
    name = f.readline()
    text = f.read()
    return (name[:-1],text[:-1])

def prepare_text( text ):
    text_copy = text;
    stemmer = SnowballStemmer('english')

    text_copy = word_tokenize(text_copy)
#    text_copy = [stemmer.stem(word) if word[0] > "Z" or word[0] < "A" else word for word in text_copy ]
    text_copy = nltk.pos_tag(text_copy)

    return text_copy

#(name, text) = read_file(raw_input('What is the name for the file to read\n'))

(name, text) = read_file(sys.argv[1])

text_proc = prepare_text(text)

#//pronoun resolution algo

sub_PR = ['he', 'she', 'me', 'my', 'i', 'him', 'her', 'himself', 'herself', 'myself']

counter = 0
recent_NNP = recent_NN = None
ref_NNP = ref_NN = None
for word in text_proc:
    if word[1] == 'NNP' or word[1] == 'NNPS':
        recent_NNP =  word
    elif word[1] == 'NN' or word[1] == 'NNS':
        recent_NN = word
    elif word[1] == 'PRP':
        if word[0].lower() in sub_PR:
            text_proc[counter] = ref_NNP
        else:
            text_proc[counter] = ref_NN
    elif word[1] == '.' or word[1] == 'CC':
        if recent_NNP:
            ref_NNP = recent_NNP
        if recent_NN:
            ref_NN = recent_NN
        recent_NNP = recent_NN = None
    counter += 1

#//actual prog
print text_proc
for word in text_proc:
    print word[0] ,

grammar = r"""
        VP: {<RB.*>*<VB.*>+<RB.*>*}
        JJP: {<JJ.*>+}
        NP:  {<DT>?<JJP>*<PRP.*>*<NN.*>}
        TY3: {<NP><VP><JJP>}
        TY1: {<NP><NP><VP>}
        TY1: {<NP><VP><NP>}
        TY1: {<NP><VP><IN><NP>}
        TY1: {<NP><VP>}
        TY3: {<JJP><NP>}

        """
cp = nltk.RegexpParser(grammar)

result = cp.parse(text_proc)

for subtree in result.subtrees():
    print subtree
    #if subtree.label() == 'TY1' or subtree.label() == 'TY3':
    #    print subtree

"""
for sent in brown.tagged_sents():
    result = cp.parse(sent)
    for subtree in result.subtrees():
        if subtree.label() == 'JUNK' : print (subtree)
"""


"""
for word in text_proc:
    print word[0] ,

example = "Sam was sitting on the couch. He is watching television. He is happy. His mom walked in the door with Hally, their dog. Hally walked right over to Sam and licked him hello."

withStopwordsRemoved = [word for word in nltk.word_tokenize(example) if word not in nltk.corpus.stopwords.words('english')]
print withStopwordsRemoved
"""
