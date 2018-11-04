from work import DictLike
from unittest import TestCase

class DictViewTestMagic(TestCase):
	d = DictLike('lol')

	def setUp(self):
		self.d.clear()

	def test_add_item(self):
		self.d['a'] = 'b'
		self.assertEqual({'a': 'b'}, self.d)

	def test_len(self):
		self.d['this'] = 'is'
		self.d['my'] = 'test'
		self.assertEqual(2, len(self.d))

	def test_contains(self):
		self.d['this'] = 'is'
		self.assertEqual(True, 'this' in self.d)
		self.assertEqual(False, 'is' in self.d)

	def test_get(self):
		self.d['this'] = 'is'
		self.assertEqual('is', self.d.get('this'))
		self.assertEqual(None, self.d.get('is'))


class DictViewTestMethods(TestCase):
	d = DictLike('lol')

	def setUp(self):
		self.d.clear()

	def test_values(self):
		self.d['Bob'] = 'Do something'
		self.d['me'] = 'I did this:)'
		self.assertEqual(['I did this:)', 'Do something'], self.d.values())

	def test_clear(self):
		self.d['this'] = 'is'
		self.d['my'] = 'test'
		self.d.clear()
		self.assertEqual({}, self.d)

	def test_items(self):
		self.d['this'] = 'is'
		self.d['my'] = 'test'
		self.assertEqual([('my', 'test'), ('this', 'is')], self.d.items())

	def test_popitem(self):
		self.d['this'] = 'is'
		self.d['my'] = 'test'
		self.d.popitem()
		self.assertEqual({'my': 'test'}, self.d)