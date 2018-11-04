import os
from collections import MutableMapping

class DictView(MutableMapping):
	def __init__(self, **kwargs):
		self.dir = './'
		[self.__setitem__(key, value) for key, value in kwargs.items() if kwargs]

	def __call__(self):
		return os.listdir(self.dir)

	def __len__(self):
		return len(os.listdir(self.dir))

	def __reversed__(self):
		return iter(os.listdir(self.dir)[::-1])

	def __contains__(self, key):
		return True if key in os.listdir(self.dir) else False

	def __iter__(self):
		return iter(os.listdir(self.dir))

	def __repr__(self):
		return f'{os.listdir(self.dir)}'

	def __getitem__(self, key):
		if key not in os.listdir(self.dir):
			raise KeyError(key)
		with open(os.path.join(self.dir, key), 'r', encoding='utf8') as f:
			return f.read()

	def __setitem__(self, key, value):
		with open(os.path.join(self.dir, key), 'w', encoding='utf8') as f:
			f.write(value)

	def __delitem__(self, key):
		if key not in os.listdir(self.dir):
			raise KeyError(key)
		os.remove(key)