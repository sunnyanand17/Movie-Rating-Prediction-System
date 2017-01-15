import re
import pickle
import csv
from nltk.corpus import stopwords
import string
import nltk

def word_feats(words):
	return dict([(word, True) for word in words])

stop = stopwords.words('english')
f = open('my_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

def score(movie_name, row):
	#print re.findall('"([^"]*)"',row)[0]
	#print "Entered"
	result={}
	raw = re.findall('"([^"]*)"',row)[0]
	#print raw
	#raw = row
	raw = re.sub(r'^https?:\/\/.*[\r\n]*', '', raw, flags=re.MULTILINE)
	comment = nltk.word_tokenize(raw)
	comment = [word for word in comment if not all(char in string.punctuation for char in word)]
	comment = [w for w in comment if w.lower() not in stop]
	comment = set(comment)
	
	
	words = word_feats(comment)
	overall = classifier.classify(word_feats(comment))
	word_polarity=[]
	for word in words:
		a=[word]
		word_polarity.append(classifier.classify(word_feats(a)))
	a,b = word_polarity.count("pos"), word_polarity.count("neg")
	total=a+b
	if overall=='pos':
		result[movie_name] = a-b
	else:
		result[movie_name]= b-a
	return result[movie_name]

#result = score("Good Kill", "Primarily this film is a debate about the ethics of drone warfare and the \"War on Terror.\" The supporting characters are representatives of political positions, their metonymic function is to parrot the arguments for and against bombing sovereign nations, collateral damage Guru,10, Mani Ratnam does it again ... outstanding!! With his vivid dramatization of the Indian business situation of the 1950s-1980s (pre-liberalization period), through the story of an ordinary entrepreneur, he surely aims at igniting the educated Indian minds towards entrepreneurship. Yes! The movie is not for everyone, but a focused audience")

#print result
