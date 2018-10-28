# tiny script to read the pickled output of coinvote.py

import pickle as pickle


class Vote:
	def __init__(self, id):
		self.id = id
		self.blocks = []
		self.addresses = []
		self.balances = []
		self.txhashes =[]
		self.vw = 0

	def calculate_vote_weight(self, coins_emitted):
		total = 0
		for b in self.balances:
			total = total + b
		self.vw = total / coins_emitted * 100
		return self.vw

# load the file

f = open('votes.db', 'rb')
votes = pickle.load(f)
f.close()

# display the votes object summary

print("QRL COINVOTE tracker:")
for i in votes:
	print("ID: ", i.id, "no. of TX: ", len(i.txhashes), "no. of Addresses: ", len(i.addresses), "Vote weight: ", i.vw, "%")

