from flask import Flask
from flask import Flask, request, jsonify
from functools import wraps
from flask import request, abort
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__)))
import utils
import logging

application = Flask(__name__)


@application.route('/get_top_tvl', methods=['POST'])
def get_top_tvl():
    top_tvl_pool = utils.get_top_tvl_all_pool()
    return {'data' : top_tvl_pool}


if __name__ == '__main__':
    application.run(host='0.0.0.0', port='8080')
