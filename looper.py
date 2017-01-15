import csv
#function that loops through each movie and checks if one of the movies in the list is present in the passed comment.
def checkEach(comment, list):
	for mov in list:
		if mov.lower() in comment.lower():
			return mov
	return ""