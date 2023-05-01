from web3 import Web3, HTTPProvider
import json
from contract import contract

class MyNFT(contract):

    def price(self):
        pass

    def mint(self, to, id, value):
        dict = {                                        # 构建一个交易的必要信息，包括发起人，接收人，传递的数值，
            'from': self.web3.eth.defaultAccount,
            'to': self.contract_address,
            'value': value
            }
        print(to)
        print(id)
        print(dict)
        tx = self.contract_instance.functions.mint(to, id).transact(dict)
        print(tx)

    def burn(self, id):
        dict = {  # 构建一个交易的必要信息，包括发起人，接收人，传递的数值，
            'from': self.web3.eth.defaultAccount,
            'to': self.contract_address
        }
        tx = self.contract_instance.functions.mint(id).transact(dict)
        print(tx)

    def isApprovedForAll(self, owner, spender):
        res = self.contract_instance.functions.isApprovedForAll(owner, spender).call()
        return res

    def supportsInterface(self, interfaceId):
        res = self.contract_instance.functions.supportsInterface(interfaceId).call()
        return res

    def ownerOf(self, id):
        res = self.contract_instance.functions.ownerOf(id).call()
        return res

    def balanceOf(self, owner):
        res = self.contract_instance.functions.balanceOf(owner).call()
        return res

    def setApprovalForAll(self, operator, approved):
        dict = {  # 构建一个交易的必要信息，包括发起人，接收人，传递的数值，
            'from': self.web3.eth.defaultAccount,
            'to': self.contract_address
        }
        tx = self.contract_instance.functions.setApprovalForAll(operator, approved).transact(dict)
        print(tx)

    def approve(self, spender, id):
        dict = {  # 构建一个交易的必要信息，包括发起人，接收人，传递的数值，
            'from': self.web3.eth.defaultAccount,
            'to': self.contract_address
        }
        tx = self.contract_instance.functions.approve(spender, id).transact(dict)
        print(tx)

    def getApproved(self, id):
        res = self.contract_instance.functions.getApproved(id).call()
        return res

    def transferFrom(self, _from, to , id):
        dict = {  # 构建一个交易的必要信息，包括发起人，接收人，传递的数值，
            'from': self.web3.eth.defaultAccount,
            'to': self.contract_address
        }
        tx = self.contract_instance.functions.transferFrom(_from, to, id).transact(dict)
        print(tx)

    def safeTransferFrom(self, _from, to ,id):
        dict = {  # 构建一个交易的必要信息，包括发起人，接收人，传递的数值，
            'from': self.web3.eth.defaultAccount,
            'to': self.contract_address
        }
        tx = self.contract_instance.functions.safeTransferFrom(_from, to, id).transact(dict)
        print(tx)

    def safeTransferFromWithData(self, _from ,to, id, data):                # 这里我不想在python的函数重载上花功夫了，所以就把名字改了下,实际上这就是上一个函数的重载，多了一个data而已
        dict = {  # 构建一个交易的必要信息，包括发起人，接收人，传递的数值，
            'from': self.web3.eth.defaultAccount,
            'to': self.contract_address
        }
        tx = self.contract_instance.functions.safeTransferFrom(_from, to, id, data).transact(dict)
        print(tx)

    def get_balance(self, address=None):
        if address is None:
            address = self.web3.eth.defaultAccount
        balance = self.web3.eth.get_balance(address)
        print('account:', self.web3.eth.defaultAccount,'balance:', balance)
        return balance


