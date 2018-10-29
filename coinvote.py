# backend script to interface with qrl-api-wrapper and the QRL network to track supplied ID's and determine coin voting %
# proof of concept, will require: error handling, db and api layers to be added for useful external function
# currently dumps the ID details (tx, balance compared to coins emitted, txhashes of specific ID message_tx) to a pickle file which coinvoteread parses output.

import q
import time
import pickle as pickle
from sc import Vote

# message_tx ID's to track in the chain

ID = ['ID_0001', 'ID_0002']

votes = []

for i in ID:
	votes.append(Vote(id=i))


# set starting blockheight to track the chain from with variable blocks

#blocks = 180450
blocks = 175000

# set safety lag in case of minor forks to chain tip

block_lag = 3


# connect to the QRL network via the api-wrapper, announce the ID's being watched..

print('COINVOTE python script')
print("ID's being tracked:", ID)

w = q.QRL()		# instantiate the grpc connection via the wrapper

blockheight = w.node_status().node_info.block_height

# continuously track ID's whilst following the current blockheight, when approaches current blockheight the script sleeps for ten minutes then resumes the chase

while blocks < blockheight:
	z = w.get_blockbynumber(blocks)
	print ('block:', blocks, len(z.block.transactions), 'transactions')
	for t in z.block.transactions:
		if t.WhichOneof('transactionType') == 'message':
			try:
				if t.message.message_hash.decode() in ID:
					addr = 'Q'+q.bin2hstr(w.get_addressfrompk(t.public_key).address)

					if len(votes[ID.index(t.message.message_hash.decode())].addresses_balances) != 0:
						if [item for item in votes[ID.index(t.message.message_hash.decode())].addresses_balances[0]] != addr:
							votes[ID.index(t.message.message_hash.decode())].addresses_balances.append((addr, w.get_balance(addr)))
					else:
						votes[ID.index(t.message.message_hash.decode())].addresses_balances.append((addr, w.get_balance(addr)))

					votes[ID.index(t.message.message_hash.decode())].blocks.append(blocks)
					votes[ID.index(t.message.message_hash.decode())].txhashes.append(t.transaction_hash)
					votes[ID.index(t.message.message_hash.decode())].calculate_vote_weight(w.node_status().coins_emitted)

					print('ID: ', t.message.message_hash.decode(), 'VOTEWEIGHT: ', votes[ID.index(t.message.message_hash.decode())].vw)

					f = open('votes.db', 'wb')
					pickle.dump(votes, f)
					f.close()
			except:
				pass

	blockheight = w.node_status().node_info.block_height
	if blocks >= blockheight - block_lag:
		print('Caught up to lag blockheight, sleeping for', block_lag, ' minutes..')
		time.sleep(60 * block_lag)
	else:
		time.sleep(0.75)
	blocks+=1

	