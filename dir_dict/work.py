import os
from collections import MutableMapping, Set

class DictView(MutableMapping):
	def __init__(self, directory='./'):
		self.dir = directory
		self.listdir = os.listdir(self.dir)

	def __call__(self):
		return {}

	def __len__(self):
		return len(self.listdir)

	def __reversed__(self):
		return iter(self.listdir[::-1])

	def __contains__(self, key):
		return True if key in self.listdir else False

	def __iter__(self):
		return iter(self.listdir)

	def __repr__(self):
		return f'{self.listdir}'

	def __getitem__(self, key):
		if key not in self.listdir:
			raise KeyError(key)
		with open(os.path.join(self.dir, key), 'r', encoding='utf8') as f:
			return f.read()

	def __setitem__(self, key):
		pass


	def __delitem__(self, key):
		if key not in self.listdir:
			raise KeyError(key)
		os.remove(key)


x = DictView()
if __name__ == "__main__":
	print(len(x))
	print(x)
	# del x['y']