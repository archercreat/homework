import os
from collections import MutableMapping

class DictLike(MutableMapping):
	def __init__(self, directory='./'):
		if not os.path.exists(directory):
			os.makedirs(directory)
		self.dir = os.path.realpath(directory)	

	def clear(self):
		for key in os.listdir(self.dir):
			self.__delitem__(key)

	def values(self):
		return [self.__getitem__(key) for key in os.listdir(self.dir)]

	def keys(self):
		return [key for key in os.listdir(self.dir)]

	def items(self):
		lst = []
		for key in os.listdir(self.dir):
			lst.append((key, self.__getitem__(key)))
		return lst

	def pop(self, key):
		self.__delitem__(key)

	def popitem(self):
		self.__delitem__(os.listdir(self.dir)[-1])

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
		buf = {}
		for key in os.listdir(self.dir):
			buf[key] = self.__getitem__(key)
		return str(buf)

	def __getitem__(self, key):
		if key not in os.listdir(self.dir):
			raise KeyError(key)
		try:
			with open(os.path.join(self.dir, key), 'r', encoding='utf8') as f:
				return f.read()
		except IsADirectoryError:
			pass

	def __setitem__(self, key, value):
		with open(os.path.join(self.dir, key), 'w', encoding='utf8') as f:
			f.write(value)

	def __delitem__(self, key):
		if key not in os.listdir(self.dir):
			raise KeyError(key)
		os.remove(self.dir + '/' + key)
