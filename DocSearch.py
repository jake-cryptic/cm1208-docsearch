import numpy as np

STOP_WORDS = ["the", "or", "it", "and", "but", "which", "on", "so", "that", "if"]


def load_file_data(file):
	with open(file) as fh:
		return [x.strip('\n') for x in fh.readlines()]


def get_words_array(string):
	return string.split(" ")


def remove_stop_words(word):
	return not word in STOP_WORDS


def main():
	doc_file = load_file_data("docs.txt")
	query_file = load_file_data("queries1.txt")

	docs = list(map(lambda x: list(filter(remove_stop_words, x)),list(map(get_words_array, doc_file))))
	queries = list(map(get_words_array, query_file))

	print(docs)
	print(queries)


if __name__ == "__main__":
	main()
