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
		print("Words in dictionary: %i" % self.corpus_word_count)

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


def main():
	corpus_data = load_file_data("docs.txt")
	query_data = load_file_data("queries1.txt")

	main_corpus = Corpus(corpus_data)
	main_corpus.build_dictionary()
	main_corpus.create_inverted_index()

	for query in query_data:
		# Output requirement
		print("Query:", query)

		relevant = main_corpus.get_relevant_docs(query)

		# Output requirement
		print("Relevant documents:", " ".join(str(d) for d in relevant))

		angles = []
		for i, doc in enumerate(main_corpus.raw_data):
			if i not in relevant: continue
			angles.append([i, main_corpus.calc_angle(doc, query)])


if __name__ == "__main__":
	main()
