from web3 import Web3, HTTPProvider
import json
from contract import contract

class Faucet(contract):

    def withdraw(self, amount, account):
        dict = {                                        # 构建一个交易的必要信息，包括发起人，接收人，传递的数值，
            'from': self.web3.eth.defaultAccount,
            'to': self.contract_address,
            }
        tx = self.contract_instance.functions.withdraw(amount, account).transact(dict)
        print(tx)

