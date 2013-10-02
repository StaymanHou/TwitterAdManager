class Gender(object):
	"""A Gender object. Currently, it's static.
	"""

	PKtoTitle = {0: 'All',
				 1: 'Male',
				 2: 'Female'}
	"""A dict convert from pk to title."""

	TitletoPK = {'All': 0,
				 'Male': 1,
				 'Female': 2}
	"""A dict convert from title to pk."""

	def __init__(self):
		super(Gender, self).__init__()
		