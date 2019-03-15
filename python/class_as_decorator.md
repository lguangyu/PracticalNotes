Class as Decorator
==================


## Minimal example

```python
class Decorator(object):
	"""
	a class as decorator must implement at minimal __init__ and __call__
	"""
	# when calls @Decorator(...), Decorator first instantiate itself:
	#   d = Decorator.__init__(...)
	# under anonymous case (@Decorator(...)), this instance becomes a closure
	def __init__(self, arg):
		super(Decorator, self).__init__()
		self.arg = arg

	# when calls @Decorator(...), Decorator first instantiate itself;
	# then use __call__ to decorate the class:
	#   @d
	#   class cls
	# equivalent to:
	#   <cls> = d.__call__(cls)
	# this creates another closure nested in the above
	# the wrapper class is from the nested closure of __call__
	# __call__ can only be in this signature
	def __call__(self, cls):
		class wrapper(cls):
			# here create class attributes of wrapper
			#class_attribute = ...

			# highly-recommended doing below:
			def __init__(deco_self, *ka, **kw):
				# this let decorated class know what originally it is
				self._decorated_original_ = cls
				super(wrapper, deco_self).__init__(*ka, **kw)

			# then create mixin methods
			def method(deco_self):
				pass
		return wrapper

	# other Decorator helper methods 

@Decorator(arg = "user args")
class Foo(object):
	def __init__(self, *ka, **kw):
		super(self._decorated_original_, self).__init__(*ka, **kw)
		pass
```

## Behavior

Above decoration is equivalent to

```python
# first instantiate a Decorator object
d = Decorator(arg = ...)

# use d for actual decoration
class Foo(object):
	pass
Foo = d(Foo)
```

It is also equivalent to function as decorator with args

```python
def decorator(arg):
	# here put lumped codes from previous Decorator class
	# ...

	def deco_handler(cls):
		class wrapper(cls):
			pass
		return wrapper
	return deco_handler
```


## Bewares

`super` call may cause problems. This can easily occur for magical methods
such as `__init__` where `super` call is typically used.
Looking at the minimal example below, minimal edition made from the minimal
example above:

```python
class Decorator(object):
	def __init__(self, arg, *ka, **kw):
		super(Decorator, self).__init__(*ka, **kw)
		self.arg = arg

	def __call__(self, cls):
		class wrapper(cls):
			arg = self.arg
			def __init__(_self, *ka, **kw):
				super(wrapper, _self).__init__(*ka, **kw)
				# so something here

			def method(_self):
				pass
		return wrapper

@Decorator("arg")
class Foo(object):
	def __init__(self, arg1, arg2):
		super(Foo, self).__init__()
		self.arg1 = arg1
		self.arg2 = arg2

if __name__ == "__main__":
	foo = Foo("arg1", "arg2")
```

The classical signature `super(cls, self)` fails with `__init__() missing two
arguments`: `arg1` and `arg2`.
Reason for this is when `super(Foo, self)` is executed, the class name `Foo` has
already bound to `wrapper`. Therefore, `super(Foo, self).__init__()` actually
called `super(wrapper, self)__init__()` which is in equivalent to
`Foo(original).__init__(arg1, arg2)`. Now you see the missing arguments issue.
Furthurmore, it actually points to a recursion issue, which leads to the actual
`Foo` initializer being called infinitly.

To solve this, one can pass the original class to the wrapper class as shown in
argument.
