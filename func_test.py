

def multi(func):

	def inner(*args,**kwargs):


		a = func(*args,**kwargs)

		return a * 2

	return inner

def divd(func):

	def inner(*args, **kwargs):

		a = func(*args,**kwargs)

		return a ** 4

	return inner

@divd
@multi
def add(a,b):

	return a+b

print(add(1,1))

