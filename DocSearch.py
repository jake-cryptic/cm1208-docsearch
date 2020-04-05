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


def get_relevant(doc_sets):
	return set.intersection(*list(map(set, doc_sets)))


class Corpus:

	def __init__(self, raw):
		self.raw_data = raw

		self.documents = {}
		self.document_words = {}

		self.inverted_index = {}
		self.corpus_words = []

		self.parse_documents()

	def parse_documents(self):
		for i, doc in enumerate(self.raw_data, 1):
			self.document_words[i] = list(filter(lambda word: not word in STOP_WORDS, get_words(doc)))

	def build_dictionary(self):
		all_words = sum(list(self.document_words.values()), [])
		self.corpus_words = list(set(all_words))
		print("Words in dictionary: %i" % len(self.corpus_words))

	def create_inverted_index(self):
		for word in self.corpus_words:
			self.inverted_index[word] = []

			for doc in self.document_words:
				if word in self.document_words[doc]:
					self.inverted_index[word].append(doc)


def main():
	corpus_data = load_file_data("docs.txt")
	query_data = load_file_data("queries1.txt")

	main_corpus = Corpus(corpus_data)
	main_corpus.build_dictionary()
	main_corpus.create_inverted_index()

	for query in query_data:
		print("Query:", query)
		relevant_docs = []

		for word in get_words(query):
			if word in main_corpus.inverted_index:
				relevant_docs.append(main_corpus.inverted_index[word])

		relevant = get_relevant(relevant_docs)

		print("Relevant documents:", " ".join(str(d) for d in relevant))


if __name__ == "__main__":
	main()
