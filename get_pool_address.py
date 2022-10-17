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

for i in range(len(top_token_list)-1):
    for j in range(i+1, len(top_token_list)-1):
        address_1, address_2 = top_token_list[i][1], top_token_list[j][1]
        symbol_1, symbol_2 = top_token_list[i][0], top_token_list[j][0]

        # get contract address for each fee: 0.05%, 0.3%, 1%
        for fee in Instance.UNISWAP_POOL_FEE:
            address_contract = contract.functions.getPool(address_1, address_2, int(fee*10000)).call()
            if address_contract != '0x0000000000000000000000000000000000000000':
                
                f.write('%s/%s/%g-%s\n'%(symbol_1, symbol_2, fee, address_contract))

