import json
import time
import random
import warnings
import requests

import core.config

warnings.filterwarnings('ignore') # Disable SSL related warnings

def requester(url, data, headers, GET, delay):
    if core.config.globalVariables['jsonData']:
        data = json.dumps(data)
    time.sleep(delay)
    user_agents = ['Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0',

    if headers:
    	if 'User-Agent' not in headers:
    		headers['User-Agent'] = random.choice(user_agents)
    if GET:
        response = requests.get(url, params=data, headers=headers, verify=False)
    elif core.config.globalVariables['jsonData']:
        response = requests.post(url, json=data, headers=headers, verify=False)
    else:
        response = requests.post(url, data=data, headers=headers, verify=False)
    return response
