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
    text_copy = nltk.pos_tag(text_copy)

    return text_copy

def process( sub, subtree ) :
    lemmatizer = WordNetLemmatizer()
    label = subtree.label();
    sub = lemmatizer.lemmatize(sub.lower(), wordnet.NOUN)
    firstNoun = ''
    secondNoun =  ''
    action =  ''
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
        return
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
                            print '3 ' + lemmatizer.lemmatize(adj[0].lower(), get_wordnet_pos( adj[1] ) )
                    break
        return
    elif label == 'TY11':
        #NP NP VP

        np = subtree[1].leaves()
        for word in np:
            if word[1].startswith('NN'):
                firstNoun = lemmatizer.lemmatize(word[0].lower(), wordnet.NOUN)

        np = subtree[0].leaves()
        for word in np:
            if word[1].startswith('NN'):
                secondNoun = lemmatizer.lemmatize(word[0].lower(), wordnet.NOUN)

        vp = subtree[2].leaves()
        for word in vp:
            if word[1].startswith('VB'):
                #action = lemmatizer.lemmatize(word[0].lower())
                action = word[0].lower()
    elif label == 'TY12':
        #NP VP NP
        np = subtree[0].leaves()
        for word in np:
            if word[1].startswith('NN'):
                firstNoun = lemmatizer.lemmatize(word[0].lower(), wordnet.NOUN)

        np = subtree[2].leaves()
        for word in np:
            if word[1].startswith('NN'):
                secondNoun = lemmatizer.lemmatize(word[0].lower(), wordnet.NOUN)

        vp = subtree[1].leaves()
        for word in vp:
            if word[1].startswith('VB'):
                #action = lemmatizer.lemmatize(word[0].lower())
                action = word[0].lower()

    elif label == 'TY13':
        # NP VP IN NP
        np = subtree[0].leaves()
        for word in np:
            if word[1].startswith('NN'):
                firstNoun = lemmatizer.lemmatize(word[0].lower(), wordnet.NOUN)

        np = subtree[3].leaves()
        for word in np:
            if word[1].startswith('NN'):
                secondNoun = lemmatizer.lemmatize(word[0].lower(), wordnet.NOUN)

        vp = subtree[1].leaves()
        for word in vp:
            if word[1].startswith('VB'):
                #action = lemmatizer.lemmatize(word[0].lower())
                action = word[0].lower()

    elif label == 'TY15':
        # NP VP
        np = subtree[0].leaves()
        for word in np:
            if word[1].startswith('NN'):
                firstNoun = lemmatizer.lemmatize(word[0].lower(), wordnet.NOUN)

        secondNoun = None

        vp = subtree[1].leaves()
        for word in vp:
            if word[1].startswith('VB'):
                #action = lemmatizer.lemmatize(word[0].lower())
                action = word[0].lower()


    if secondNoun is None:
        print '1 ' + action
    elif firstNoun == sub:
        #1 action secondnoun
        print '1 ' + action + ' ' + secondNoun
    elif secondNoun == sub:
        #2 action firstnoun
        print '2 ' + action + ' ' + firstNoun
    return


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



(name, text) = read_file(sys.argv[1])

text_proc = prepare_text(text)

#pronoun resolution algo

sub_PR = ['he', 'she', 'me', 'my', 'i', 'him', 'her', 'himself', 'herself', 'myself', 'themselves']

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

#actual prog

grammar = r"""
        VP: {<W.*>*<RB.*>*<VB.*>+<RB.*>*}
        JJP: {<JJ.*|CC>+}
        NP:  {<DT>?<JJP>*<PRP.*>*<NN.*>}
        TY31: {<NP><VP><JJP>}
        TY11: {<NP><NP><VP>}
        TY12: {<NP><VP><NP>}
        TY13: {<NP><VP><IN><NP>}
        TY15: {<NP><VP>}
        TY32: {<JJP><NP>}
       """
cp = nltk.RegexpParser(grammar)

result = cp.parse(text_proc)

for subtree in result.subtrees():
    if subtree.label() != 'VP' and subtree.label() != 'NP' and subtree.label() != 'JJP' and subtree.label() != 'S':
        process(name, subtree)

