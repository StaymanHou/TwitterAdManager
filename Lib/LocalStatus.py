class LocalStatus(object):
	"""docstring for LocalStatus"""

	PKtoTitle = {1: 'Dead',
				 2: 'Alive',
				 3: 'CreatePending',
				 4: 'DeletePending',
				 5: 'CreateFail',
				 6: 'DeleteFail'}

	TitletoPK = {'Dead': 1,
				 'Alive': 2,
				 'CreatePending': 3,
				 'DeletePending': 4,
				 'CreateFail': 5,
				 'DeleteFail': 6}

	def __init__(self):
		super(LocalStatus, self).__init__()
		