from web3 import Web3
from collections import namedtuple
import sys
import os
import utils
sys.path.append(os.path.join(os.path.dirname(__file__)))
import Instance

# 0. init
web3 = utils.init_web3_conntection()

abi = utils.read_json_file('data/v3_pool_abi.json')

token_price_list = utils.get_current_price_of_list_tokens(web3, pool_list)
print(token_price_list)



def get_tvl_all_pool():
    pool_list = utils.read_pool_list_csv_file('data/list_pool.csv')
    token_price_list = utils.get_current_price_of_list_tokens(web3, pool_list)

    for token1, list_pool_info in pool_list.items():
        for token2, pool_info in list_pool_info.items():
            for i in range(pool_info):
                fee, pool_address = pool_info[i]['fee'], pool_info[i]['pool_address']
                token_1_balance = utils.get_token_balance_of_contract(web3, token1, pool_address)
                token_2_balance = utils.get_token_balance_of_contract(web3, token2, pool_address)

                tvl = token_1_balance * token_price_list[token1] + token_2_balance * token_price_list[token2]
                pool_list 