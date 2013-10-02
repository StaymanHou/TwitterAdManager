class LocalStatus(object):
	"""A LocalStatus object. Currently, it's static.
	"""

	PKtoTitle = {1: 'Dead',
				 2: 'Alive',
				 3: 'CreatePending',
				 4: 'DeletePending',
				 5: 'CreateFail',
				 6: 'DeleteFail'}
	"""A dict convert from pk to title."""

	TitletoPK = {'Dead': 1,
				 'Alive': 2,
				 'CreatePending': 3,
				 'DeletePending': 4,
				 'CreateFail': 5,
				 'DeleteFail': 6}
	"""A dict convert from title to pk."""

	def __init__(self):
		super(LocalStatus, self).__init__()
		