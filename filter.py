import re
#import score
import looper
from operator import add
import os
import sys
execfile("final_score.py")

#setClassPath()

from pyspark import SparkContext
sc = SparkContext(appName="Rating")

#no idea how to run with pyspark
#list of movie names
movieList = sc.textFile("movielist.txt")
#convert to a broadcast variable
broadMovies = sc.broadcast(movieList.collect())
#comments from movie subreddits
comments = sc.textFile("comments.csv")
#score.init()
#<comment, entire row>
keyComments = comments.map(lambda part : (re.findall('"([^"]*)"',part),part)).filter(lambda x : len(x[0])>0).map(lambda y : (y[0][0],y[1]))


#apply the function to each comment and filter which have movies in them. Output is <moviename, entire row>	
comm = keyComments.map(lambda x : (looper.checkEach(x[0], broadMovies.value),x[1])).filter(lambda y : len(y[0])>0)

# group movies by movie name. <moviename, List[row1, row2, ...]>
#Get the average rating for every movie. 
#RULES:
#1. A like is a rating.
#2. We need at least 5 ratings for a movie to consider it.
nlpMovies = comm.map(lambda x : (x[0], (score(x[0],x[1])*int(x[1].split(",")[15]), int(x[1].split(",")[15])))).reduceByKey(lambda a,b: (a[0] + b[0], a[1] + b[1]))\
                    .filter(lambda x : x[1][1] >= 5).map(lambda x: (x[0], x[1][0]/x[1][1]))

minScore = nlpMovies.map(lambda x: x[1]).min()
maxScore = nlpMovies.map(lambda x: x[1]).max()

#We have considered only the good movies in movie history. Adding a correction factor of 4.
normalizedScores = nlpMovies.map(lambda x: (x[0], 4 + (x[1] - minScore)*5.0/(maxScore - minScore)))

print normalizedScores.collectAsMap()

