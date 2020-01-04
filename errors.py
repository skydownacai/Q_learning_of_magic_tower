class BaseError(Exception): # pragma: no cover
	"""Generic error wrapper."""
	def __init__(self, msg):
		self._msg = msg

	def __str__(self):

		return repr(self._msg)


class invalid_attribution(BaseError):

	def __init__(self):

		super().__init__(msg = "This Object doesn't have this attribution!")

class type_error(BaseError):

	def __init__(self,msg):

		super().__init__(msg = msg)

class value_error(BaseError):

	def __init__(self,msg):

		super().__init__(msg = msg)

class End_Game(BaseError):

	def __init__(self):

		pass
class Death(BaseError):

	def __init__(self):

		pass

class NoWarrior(BaseError):

	def __init__(self):

		super().__init__(msg = "You haven't sepecific a warrior to act with. Try : Action.warrior =  warrior()")
