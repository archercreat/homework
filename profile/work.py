from functools import wraps
from datetime import datetime
import time

def profile(func):
	@wraps(func)
	def new_func(*args, **kwargs):
		name = new_func.__name__
		print(f'`{name}` started')
		start = datetime.now().timestamp()
		result =  func(*args, **kwargs)
		stop = datetime.now().timestamp()
		print('`%s` finished in %f sec' % (new_func.__name__, stop - start))
		return result
	return new_func

def time_all_class_methods(Cls):
	class NewCls:
		def __init__(self,*args,**kwargs):
			self.oInstance = Cls(*args,**kwargs)
		def __getattribute__(self,s):
			try:
				x = super(NewCls,self).__getattribute__(s)
			except AttributeError:
				pass
			else:
				return x
			x = self.oInstance.__getattribute__(s)
			if type(x) == type(self.__init__):
				return time_this(x)
			else:
				return x

	def time_this(original_function):
		def new_function(*args,**kwargs):
			from datetime import datetime
			before = datetime.now()
			result = original_function(*args,**kwargs)
			after = datetime.now()
			print("Elapsed Time = {0}".format(after-before))
			return result
		return new_function
	return NewCls



@time_all_class_methods
def foo(x, y):
	return x + y

@time_all_class_methods
class Bar:
	def __init__(self):
		self.name = 'Bob'
		self.age  = '20'

	def rofl(self):
		time.sleep(3)
		return 'LOL'

oF = Bar()
print(oF.rofl())
print(foo(1, 2))
