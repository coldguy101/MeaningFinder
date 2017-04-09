from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
import nltk

def read_file( filename ):
    f = open(filename, 'r')
    name = f.readline()
    text = f.read()
    return (name[:-1],text[:-1])

def prepare_text( text ):
    text_copy = text;
    stemmer = SnowballStemmer('english')

    text_copy = word_tokenize(text_copy)
    #text_copy = [stemmer.stem(word) for word in text_copy]
    text_copy = nltk.pos_tag(text_copy)

    return text_copy

(name, text) = read_file(raw_input('What is the name for the file to read\n'))


text_proc = prepare_text(text)


//pronoun resolution algo

//actual prog


print text_proc

example = "Sam was sitting on the couch. He is watching television. He is happy. His mom walked in the door with Hally, their dog. Hally walked right over to Sam and licked him hello."

withStopwordsRemoved = [word for word in nltk.word_tokenize(example) if word not in nltk.corpus.stopwords.words('english')]

print withStopwordsRemoved
