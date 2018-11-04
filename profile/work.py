def profile(obj):
	from functools import wraps
	from datetime import datetime
	import inspect

	def func_wrapper(func):
		@wraps(func)
		def new_func(*args, **kwargs):
			print(f'`{func.__name__}` started')
			start = datetime.now().timestamp()
			result = func(*args, **kwargs)
			stop = datetime.now().timestamp()
			print('`%s` finished in %f'% (func.__name__, stop - start))
			return result
		return new_func

	def class_wrapper(klass):
		class_objs = [(name, obj) for name, obj in klass.__dict__.items() if inspect.isfunction(obj)]
		for class_obj in class_objs:
			name, _ = class_obj
			attr = getattr(klass, name)
			setattr(klass, name, func_wrapper(attr))
		return klass

	if inspect.isfunction(obj):
		return func_wrapper(obj)
	elif inspect.isclass(obj):
		return class_wrapper(obj)


@profile
def foo(x, y):
	return x + y

@profile
class Bar:
	def __init__(self):
		self.name = 'Bob'
		self.age  = '20'

	def rofl(self):
		return 'LOL'

	def mom(self):
		return 'KEK'

oF = Bar()
print(oF.rofl())
print(oF.mom())
print(foo(1, 2))