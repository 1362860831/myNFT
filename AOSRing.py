from web3 import Web3, HTTPProvider
import json
from contract import contract

class AOSRing(contract):
    def Verify(self, pubkeys, tees, seed, message):
        dict = {                                        # 构建一个交易的必要信息，包括发起人，接收人，传递的数值，
            'from': self.web3.eth.defaultAccount,
            'to': self.contract_address,
            }
        res = self.contract_instance.functions.Verify(pubkeys, tees, seed, message).call()
        return res
