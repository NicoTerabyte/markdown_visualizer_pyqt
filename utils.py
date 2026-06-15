'''
given a word (occurrence) count how many times that word appears in the text
since count would give a strange number without occurrence i set it to zero
if there's no occurrence
'''
def total_of_occurencies(text: str, occurrence: str):
	if occurrence != "":
		total_occurrences = text.count(occurrence)
	else:
		total_occurrences = 0
	return total_occurrences
