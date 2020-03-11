import numpy as np


def load_file_data(file):
	with open(file) as fh:
		return [x.strip('\n') for x in fh.readlines()]


def main():
	print(load_file_data("docs.txt"))
	print(load_file_data("queries1.txt"))


if __name__ == "__main__":
	main()
