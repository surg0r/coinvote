
class Vote:
	def __init__(self, id):
		self.id = id
		self.blocks = []
		self.addresses_balances = []
		self.txhashes =[]
		self.vw = 0

	def calculate_vote_weight(self, coins_emitted):
		total = 0
		for b in self.addresses_balances:
			total = total + b[1]
		self.vw = total / coins_emitted * 100
		self.total = total
		return self.vw

	def update_balances(self, qrl_connector):
		temp_list = []
		for b in self.addresses_balances:
			z = (b[0], qrl_connector.get_balance(b[0]))
			temp_list.append(z)

		self.addresses_balances = temp_list