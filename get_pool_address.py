from web3 import Web3
from collections import namedtuple
import sys
import os
import utils
sys.path.append(os.path.join(os.path.dirname(__file__)))
import Instance

"""
https://etherscan.io/address/0x1f98431c8ad98523631ae4a59f267346ea31f984#code
get pool address by call function getPool
"""

# 0. init
web3 = utils.init_web3_conntection()

abi = utils.read_json_file('data/factory_abi.json')

contract = web3.eth.contract(address=Instance.FACTORY_POOL_ADDRESS, abi=abi)

f = open('data/list_pool.csv', 'w')


# 1. get pool address for each pairs

top_token_list = Instance.TOP_TOKEN

for i, (token1, token1_info) in enumerate(top_token_list.items()):
    for j, (token2, token2_info) in enumerate(top_token_list.items()):
        if i < j:
            address_1, address_2 = token1_info['address'], token2_info['address']

            # get contract address for each fee: 0.05%, 0.3%, 1%
            for fee in Instance.UNISWAP_POOL_FEE:
                address_contract = contract.functions.getPool(address_1, address_2, int(fee*10000)).call()
                if address_contract != Instance.NULL_ADDRESS:
                    token_balance_1 = utils.get_token_balance_of_contract(web3, token1, address_contract)
                    token_balance_2 = utils.get_token_balance_of_contract(web3, token2, address_contract)
                    if token_balance_1 > 100*(10**token1_info['decimal']) or token_balance_2 > 100*(10**token2_info['decimal']): # filter out small pool
                        f.write('%s-%s-%g-%s\n'%(token1, token2, fee, address_contract))

