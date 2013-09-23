class Gender(object):
	"""docstring for Gender"""

	PKtoTitle = {0: 'All',
				 1: 'Male',
				 2: 'Female'}

	TitletoPK = {'All': 0,
				 'Male': 1,
				 'Female': 2}

	def __init__(self):
		super(Gender, self).__init__()
		