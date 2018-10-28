# qrl-api-wrapper
# needs error handling!

import qrl_pb2, qrl_pb2_grpc
import grpc
from pyqrllib.pyqrllib import bin2hstr, hstr2bin, bin2mnemonic, sha2_256, ucharVector, shake256, QRLDescriptor
from pyqrllib import pyqrllib

from os import urandom

# minor string functions

def hstr2bin_bytes(hstr):
    return bytes(hstr2bin(hstr))


# grpc functions accessible within a class

class QRL():
    def __init__(self, node='35.178.79.137:19009', verbose=False):                  #may be overriden with local node
        self.grpc_connect(node)

    def grpc_connect(self,node):
        self.channel = grpc.insecure_channel(node)
        self.stub = qrl_pb2_grpc.PublicAPIStub(self.channel)

    def node_status(self):
        return self.stub.GetStats(qrl_pb2.GetStatsReq())

    def get_address_state(self, address, exclude_ots_bitfield=False, exclude_transaction_hashes=False):
        addr = self.stub.GetAddressState(qrl_pb2.GetAddressStateReq(address=hstr2bin_bytes(address[1:]),exclude_ots_bitfield=exclude_ots_bitfield, exclude_transaction_hashes=exclude_transaction_hashes))
        return addr

    def get_address_state2(self, address):
        addr = self.stub.GetAddressState(qrl_pb2.GetAddressStateReq(address=hstr2bin_bytes(address[1:])))
        return addr

    def get_addressfrompk(self, pk):        #bytes pk
        addr = self.stub.GetAddressFromPK(qrl_pb2.GetAddressFromPKReq(pk=pk))
        return addr

    def parse_address(self, address):
        addr = self.stub.ParseAddress(qrl_pb2.ParseAddressReq(address=hstr2bin_bytes(address[1:])))
        return addr

    def get_peers_state(self):
        return self.stub.GetPeersStat(qrl_pb2.GetPeersStatReq())

    def chain_stats(self,include_timeseries):
        return self.stub.GetStats(qrl_pb2.GetStatsReq(include_timeseries=include_timeseries))

    def get_peers_list(self):
        knownpeers = self.stub.GetKnownPeers(qrl_pb2.GetKnownPeersReq())
        self.peers = []
        for p in knownpeers.known_peers:
            self.peers.append(p.ip)
        return self.peers

    def get_object(self, some_obj):
        obj = self.stub.GetObject(qrl_pb2.GetObjectReq(query=bytes(some_obj)))
        #if obj.found == True:
        #   return obj#.address_state                              # obj.address_state.address/nonce/pubhashes/transaction_hashes
        #else:
         #   return False
        return obj

    def get_balance(self, address):
        return self.stub.GetBalance(qrl_pb2.GetBalanceReq(address=hstr2bin_bytes(address[1:]))).balance

    def get_blockbynumber(self, block_number):
        block_obj = self.stub.GetBlockByNumber(qrl_pb2.GetBlockByNumberReq(block_number=block_number))
        return block_obj

    def grpc_PushTransaction(self, tx_obj):
        response = self.stub.PushTransaction(qrl_pb2.PushTransactionReq(transaction_signed=tx_obj))
        return response
