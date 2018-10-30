from functools import reduce


class TextHistory:

	def __init__(self, text='', version=0):
		self._text = text
		self._version = version
		self._history = []

	@property
	def text(self):
		return self._text

	@property
	def version(self):
		return self._version

	def action(self, job):
		if job.from_version != self._version:
			raise ValueError('versions does not match')
		self._text = job.apply(self._text)
		self._version = job.to_version
		self._history.append(job)
		return job.to_version

	def optimization(self, first, second):
		# print(type(first))
		prev = first[-1] if len(first) else None
		if type(prev) is InsertAction and type(second) is InsertAction:
			if prev._pos + len(prev._text) == second.pos:
				return first[:-1] + [InsertAction(prev._pos, prev._text + second._text, prev.from_version, second.to_version)]

		if type(prev) is ReplaceAction and type(second) is ReplaceAction:
			if prev._pos + len(prev._text) == second.pos:
				return first[:-1] + [ReplaceAction(prev._pos, prev._text + second._text, prev.from_version, second.to_version)]

		if type(prev) is DeleteAction and type(second) is DeleteAction:
			if prev._pos == second._pos:
				return first[:-1] + [DeleteAction(prev._pos, prev._length + second._length, prev.from_version, second.to_version)]
		return first + [second]

	def get_actions(self, from_version=0, to_version=None):
		if to_version is None:
			to_version = self._version
		if from_version > to_version or from_version < 0 or to_version < 0 or to_version > self._version:
			raise ValueError('wrong get_actions params')

		return list(reduce(self.optimization, self._history[from_version:to_version], []))


	def insert(self, text, pos=None):
		if pos is None:
			pos = len(self._text)
		job = InsertAction(pos, text, self._version, self._version+1)
		return self.action(job)

	def delete(self, pos, length):
		job = DeleteAction(pos, length, self._version, self._version+1)
		return self.action(job)

	def replace(self, text, pos=None):
		if pos is None:
			pos = len(self._text)
		job = ReplaceAction(pos, text, self._version, self._version+1)
		return self.action(job)





class Action(object):
	def __init__(self, from_version, to_version):
		if from_version > to_version:
			raise ValueError('wrong version')
		self._from_version = from_version
		self._to_version = to_version

	@property
	def from_version(self):
		return self._from_version

	@property
	def to_version(self):
		return self._to_version
	


class InsertAction(Action):
	def __init__(self, pos, text, from_version, to_version):
		self._pos = pos
		self._text = text
		super().__init__(from_version, to_version)

	@property
	def text(self):
		return self._text
	
	@property
	def pos(self):
		return self._pos

	def __repr__(self):
		return f'InsertAction(pos={self._pos}, text={self._text}, from_version={self.from_version}, to_version={self.to_version})'

	def apply(self, string):
		if self._pos < 0 or self._pos > len(string):
			raise ValueError('wrong position to insert')
		return string[:self._pos] + self._text + string[self._pos:]





class ReplaceAction(Action):
	def __init__(self, pos, text, from_version, to_version):
		self._pos = pos
		self._text = text
		super().__init__(from_version, to_version)

	@property
	def pos(self):
		return self._pos
	
	@property
	def text(self):
		return self._text

	def __repr__(self):
		return f'ReplaceAction(pos{self._pos}, text={self._text}, from_version={self.from_version}, to_version={self.to_version})'
	
	def apply(self, string):
		if self._pos > len(string) or self._pos < 0:
			raise ValueError('wrong position to replace')
		return string[:self._pos] + self._text + string[self._pos+len(self._text):]



class DeleteAction(Action):
	def __init__(self, pos, length, from_version, to_version):
		self._pos = pos
		self._length = length
		super().__init__(from_version, to_version)

	@property
	def pos(self):
		return self._pos
	
	@property
	def length(self):
		return self._length

	def __repr__(self):
		return f'DeleteAction(pos={self._pos}, length={self._length}, from_version={self.from_version}, to_version{self.to_version})'

	def apply(self, string):
		if self._pos < 0 or self._pos > len(string):
			raise ValueError('wrong position to delete')
		if self._length + self._pos > len(string):
			raise ValueError('wrong length to delete')
		return string[:self._pos] + string[self._pos+self._length:]



def main():
	
	h = TextHistory()
	h.insert('deadbeef')
	h.insert(' cafebabe')
	print(h._text)
	h.replace('l', 4)
	h.replace('mao', 5)
	print(h._text)
	h.delete(4, 8)
	print(h._text)
	h.delete(4, 2)
	print(h._text)
	action = h.get_actions(0)
	for i in action:
		print(i)


if __name__ == '__main__':
	main()