from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
import nltk
import sys

def read_file( filename ):
    f = open(filename, 'r')
    name = f.readline()
    text = f.read()
    return (name[:-1],text[:-1])

def prepare_textext( text ):
    text_copy = text;
    stemmer = SnowballStemmer('english')

    text_copy = word_tokenize(text_copy)
    text_copy = [stemmer.stem(word) if word[0] > "Z" or word[0] < "A" else word for word in text_copy ]
    text_copy = nltk.pos_tag(text_copy)

    return text_copy

#(name, text) = read_file(raw_input('What is the name for the file to read\n'))

(name, text) = read_file(sys.argv[1])

for word in text:
    print word[0] ,

text_proc = prepare_text(text)

for word in text_proc:
    print word[0] ,

#//pronoun resolution algo

sub_PR = ['he', 'she', 'me', 'my', 'i', 'him', 'her', 'himself', 'herself', 'myself']

counter = 0
recent_NNP = recent_NN = None
ref_NNP = ref_NN = None
for word in text_proc:
    if word[1] == 'NNP':
        recent_NNP =  word
    elif word[1] == 'NN':
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

for word in text_proc:
    print word[0] ,

"""
example = "Sam was sitting on the couch. He is watching television. He is happy. His mom walked in the door with Hally, their dog. Hally walked right over to Sam and licked him hello."

withStopwordsRemoved = [word for word in nltk.word_tokenize(example) if word not in nltk.corpus.stopwords.words('english')]
print withStopwordsRemoved
"""
