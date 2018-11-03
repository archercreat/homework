from functools import wraps
import time


def profile(func):
	for attr_name in func.__dict__:
		# print(getattr(func, attr_name))
		pass
	@wraps(func)
	def new_func(*args, **kwargs):
		name = new_func.__name__
		print(f'`{name}` started')
		start = time.time()
		result =  func(*args, **kwargs)
		stop = time.time()
		print('`%s` finished in %2.2f sec' % (new_func.__name__, stop - start))
		return result

	return new_func

@profile
def foo(x, y):
	return x + y

@profile
class Bar:
	def __init__(self):
		self.name = 'Bob'
		self.age  = '20'

	def __call__(self):
		return self.name

foo(1, 2)