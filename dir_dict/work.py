import os
from collections import MutableMapping, Set


class DictView:
	def __init__(self):
		pass

	def __call__(self):
		return {}

	def __len__(self):
		return len(os.listdir())


if __name__ == "__main__":
	print(len(DictView()))