"""
"	CM1208 - Maths for Computer Science
"	Jake Mcneill
"	c1931370
"""

import numpy as np

STOP_WORDS = ["the", "or", "it", "and", "but", "which", "on", "so", "that", "if"]


def load_file_data(file):
	with open(file) as fh:
		return [x.strip('\n') for x in fh.readlines()]


def get_words(string):
	return string.split(" ")


class Corpus:

	def __init__(self, raw):
		self.raw_data = raw

		self.documents = {}
		self.document_words = {}

		self.inverted_index = {}
		self.corpus_words = []
		self.corpus_word_count = 0

		self.parse_documents()

	def parse_documents(self):
		for i, doc in enumerate(self.raw_data, 1):
			self.document_words[i] = list(filter(lambda word: not word in STOP_WORDS, get_words(doc)))

	def build_dictionary(self):
		all_words = sum(list(self.document_words.values()), [])
		self.corpus_words = list(set(all_words))
		self.corpus_word_count = len(self.corpus_words)

	def create_inverted_index(self):
		for word in self.corpus_words:
			self.inverted_index[word] = []

			for doc in self.document_words:
				if word in self.document_words[doc]:
					self.inverted_index[word].append(doc)

	def get_relevant_docs(self, query):
		relevant_docs = []

		for word in get_words(query):
			if word in self.inverted_index:
				relevant_docs.append(self.inverted_index[word])

		relevant_docs_set = list(map(set, relevant_docs))

		return set.intersection(*relevant_docs_set)

	def calc_angle(self, doc, query):
		doc_words = get_words(doc)
		query_words = get_words(query)

		# https://docs.scipy.org/doc/numpy/reference/generated/numpy.zeros.html
		# Change default dtype to int as by default is float64
		doc_vector = np.zeros(self.corpus_word_count, dtype=np.int)
		query_vector = np.zeros(self.corpus_word_count, dtype=np.int)

		for i, word in enumerate(self.corpus_words):
			doc_vector[i] = doc_words.count(word)
			query_vector[i] = query_words.count(word)

		size = np.linalg.norm(doc_vector) * np.linalg.norm(query_vector)

		# Angle must be returned in degrees as specified
		return np.degrees(
			np.arccos(
				np.dot(doc_vector, query_vector) / size
			)
		)


def main():
	corpus_data = load_file_data("docs.txt")
	query_data = load_file_data("queries1.txt")

	main_corpus = Corpus(corpus_data)
	main_corpus.build_dictionary()
	main_corpus.create_inverted_index()

	# Output requirement
	print("Words in dictionary: %i" % main_corpus.corpus_word_count)

	for query in query_data:
		# Output requirement
		print("Query:", query)

		list_of_doc_ids = main_corpus.get_relevant_docs(query)

		# Output requirement
		print("Relevant documents:", " ".join(str(doc_id) for doc_id in list_of_doc_ids))

		# Calculate angles
		calculated_angles = []
		for i, doc in enumerate(main_corpus.raw_data, 1):
			if i in list_of_doc_ids:
				calculated_angles.append([i, main_corpus.calc_angle(doc, query)])

		print(calculated_angles)
		calculated_angles.sort(key=lambda x: x[1])
		print(calculated_angles)

		for data in calculated_angles:
			angle = round(data[1], 2)
			print("%s %s" % (data[0], angle))



if __name__ == "__main__":
	main()
