# tiny script to read the pickled output of coinvote.py

import pickle as pickle
import q
from sc import Vote

# load the file

f = open('votes.db', 'rb')
votes = pickle.load(f)
f.close()

# connect to the qrl

w = q.QRL()		# instantiate the grpc connection via the wrapper


# update balances based upon realtime data from the list of addresses in each message_tx ID
# calculate vote weighting..

for v in votes:
	v.update_balances(w)
	v.calculate_vote_weight(w.node_status().coins_emitted)

print("QRL COINVOTE tracker:")
for i in votes:
	print("ID: ", i.id, "no. of TX: ", len(i.txhashes), "no. of Addresses: ", len(i.addresses_balances),'supporting coins: ', (i.total / 10 ** 9), "Vote weight: ", round(i.vw, 6), "%")

