import json
from web3 import Web3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
import Instance
from dotenv import load_dotenv
load_dotenv()

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
            split_str = line.split("-")
            pool_list[split_str[0]] = split_str[1]
        
        return pool_list


def init_web3_conntection():
    web3 = Web3(Web3.HTTPProvider(os.getenv('INFURA_ENPOINT')))
    return web3