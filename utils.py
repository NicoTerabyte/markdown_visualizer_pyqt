import cython

'''
given a word (occurrence) count how many times that word appears in the text
since count would give a strange number without occurrence i set it to zero
if there's no occurrence.

To count properly with the count method i have to make the text and the occurence string
or lowercase or uppercase since count is case sensitive
'''

def count_occurrences(text: str, occurrence: str):
	text = text.lower()
	occurrence = occurrence.lower()
	total_occurrences = cython.declare(cython.int, 0)
	if occurrence != "":
		print("counting")
		total_occurrences = text.count(occurrence)
	return total_occurrences
