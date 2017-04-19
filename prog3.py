from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
from nltk import tree
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

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

def process( sub, subtree ) :
    lemmatizer = WordNetLemmatizer()
    label = subtree.label();
    sub = lemmatizer.lemmatize(sub.lower(), wordnet.NOUN)
    #print sub
    if label == 'TY31':
        #Checks if the chunk is important
        np = subtree[0].leaves()

        for word in np:
            if word[1].startswith('NN'):
                if  lemmatizer.lemmatize(word[0].lower(), get_wordnet_pos( word[1] )) == sub:
                    part = subtree[2]
                    part = part.leaves()
                    for adj in part:
                        if adj[1].startswith('J'):
                            print '3 ' + lemmatizer.lemmatize(adj[0], get_wordnet_pos( adj[1] ) )
                    break
    elif label == 'TY32':
        #Checks if the chunk is important
        np = subtree[1].leaves()

        for word in np:
            if word[1].startswith('NN'):
                if  lemmatizer.lemmatize(word[0].lower(), get_wordnet_pos( word[1] )) == sub:
                    part = subtree[0]
                    part = part.leaves()
                    for adj in part:
                        if adj[1].startswith('J'):
                            print '3 ' + lemmatizer.lemmatize(adj[0], get_wordnet_pos( adj[1] ) )
                    break

def get_wordnet_pos( tag ):
    if tag.startswith('J') :
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


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

grammar = r"""
        VP: {<W.*>*<RB.*>*<VB.*>+<RB.*>*}
        JJP: {<JJ.*|CC>+}
        NP:  {<DT>?<JJP>*<PRP.*>*<NN.*>}
        TY31: {<NP><VP><JJP>}
        TY11: {<NP><NP><VP>}
        TY12: {<NP><VP><NP>}
        TY13: {<NP><VP><IN><NP>}
        TY14: {<TY1.*><VP><NP>}
        TY15: {<NP><VP>}
        TY32: {<JJP><NP>}
       """
cp = nltk.RegexpParser(grammar)

result = cp.parse(text_proc)

for subtree in result.subtrees():
    if subtree.label() != 'VP' and subtree.label() != 'NP' and subtree.label() != 'JJP' and subtree.label() != 'S':
        process(name, subtree)
        #print subtree

"""
print text_proc
for word in text_proc:
    print word[0] ,
"""


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
