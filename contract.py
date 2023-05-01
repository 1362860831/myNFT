from web3 import Web3, HTTPProvider
import json

class contract:
    def __init__(self, _entroypoint, _truffleFile, _contract_address,  _name, _account=None):
        self.entrypoint = _entroypoint
        self.web3 = Web3(HTTPProvider(self.entrypoint))                                 # 这里有一个小问题，这么写的话等于每一次创建一个SimpleAuction都会创建一个新的链接，也有可能会因为网站负荷导致链接挂掉。正常操作的话其实是倾向于使用一个链接池解决这个问题

        if _account is None:
            self.web3.eth.defaultAccount = self.web3.eth.accounts[0]                        # 这里请注意，defaultAccount最好要进行修改
        else:
            self.web3.eth.defaultAccount = _account
            self.web3.geth.personal.unlock_account(_account, _name)

        self.contract_address = _contract_address
        truffleFile = json.load(open(_truffleFile))
        abi = truffleFile['abi']
        self.contract_instance = self.web3.eth.contract(abi=abi, address=self.contract_address)