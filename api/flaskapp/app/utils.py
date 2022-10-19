from audioop import add
import json
from tkinter import INSERT
from web3 import Web3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
import Instance
from dotenv import load_dotenv
load_dotenv()
BASE_DATA_FOLDER = os.getenv('BASE_DATA_FOLDER')

def read_json_file(file_path: str):
    try:
        f_ = open(file_path, 'r')
    except Exception as e:
        raise e
    else:
        json_data = json.loads(f_.read())
    return json_data

def read_pool_list_csv_file(file_path: str):
    
    try:
        f_ = open(file_path, 'r')
    except Exception as e:
        raise e
    else:
        lines = f_.readlines()
        pool_list = {}
        for line in lines:
            pool_info = line.split("-")
            token1, token2, fee, address = pool_info[0], pool_info[1], pool_info[2], pool_info[3]
            if token1 not in pool_list:
                pool_list[token1] = {}
            if token2 not in pool_list[token1]:
                pool_list[token1][token2] = []

            pool_list[token1][token2].append({'fee': fee, 'pool_address': address.strip()})
        
        return pool_list


def init_web3_conntection():
    web3 = Web3(Web3.HTTPProvider(os.getenv('INFURA_ENPOINT')))
    return web3

def get_token_balance_of_contract(web3: Web3, token_symbol: str, contract_address: str):
    abi = read_json_file('%s/token_abi.json'%BASE_DATA_FOLDER)
    token_address, token_decimal = Instance.TOP_TOKEN[token_symbol]['address'], Instance.TOP_TOKEN[token_symbol]['decimal']
    token_balance_x = web3.eth.contract(address=token_address, abi=abi).functions.balanceOf(contract_address).call()
    token_balance = token_balance_x / (10**token_decimal)
    return token_balance

def get_current_price_of_token(web3: Web3, pool_address: str, abi: json, decimal_diff: int):
    USDC_address = Instance.TOP_TOKEN['USDC']['address']
    contract = web3.eth.contract(address=pool_address, abi=abi)
    slot0 = contract.functions.slot0().call()
    token0_address = contract.functions.token0().call()
    sqrtPriceCurrent = slot0[0] / (1 << 96)
    priceCurrent = sqrtPriceCurrent ** 2

    if token0_address == USDC_address:
        return 10**(-decimal_diff)/( priceCurrent) 
    else:
        return priceCurrent/(10**decimal_diff)

def get_current_price_of_list_tokens(web3: Web3, pool_list: dict ):
    abi = read_json_file('%s/v3_pool_abi.json'%BASE_DATA_FOLDER)
    list_token = Instance.TOP_TOKEN
    token_price_list = {'USDC': 1}
    for  token in pool_list['USDC'].keys():
        price = get_current_price_of_token(web3, pool_list['USDC'][token][0]['pool_address'], abi, list_token['USDC']['decimal'] - list_token[token]['decimal'])
        token_price_list[token] = price 

    return token_price_list

def get_top_tvl_all_pool():
    #init

    web3 = init_web3_conntection()
    pool_list = read_pool_list_csv_file('%s/list_pool.csv'%BASE_DATA_FOLDER)
    tvl_pool = {}

    # get token price of each token    
    token_price_list = get_current_price_of_list_tokens(web3, pool_list)


    for token1, list_pool_info in pool_list.items():
        for token2, pool_info in list_pool_info.items():
            for i in range(len(pool_info)):
                
                fee, pool_address = pool_info[i]['fee'], pool_info[i]['pool_address']
                token_1_balance = get_token_balance_of_contract(web3, token1, pool_address)
                token_2_balance = get_token_balance_of_contract(web3, token2, pool_address)

                tvl = token_1_balance * token_price_list[token1] + token_2_balance * token_price_list[token2]
                tvl_pool['%s/%s/%s'%(token1,token2,fee)] = {'tvl': tvl, 'address': pool_address}
               

    sorted_tvl_pool = sorted(tvl_pool.items(),  key=lambda item: item[1]['tvl'], reverse=True )

    return sorted_tvl_pool