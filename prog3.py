import nltk;

example = "Sam was sitting on the couch. He is watching television. He is happy. His mom walked in the door with Hally, their dog. Hally walked right over to Sam and licked him hello."

withStopwordsRemoved = [word for word in nltk.word_tokenize(example) if word not in nltk.corpus.stopwords.words('english')]

print withStopwordsRemoved