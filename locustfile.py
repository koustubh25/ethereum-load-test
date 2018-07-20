#!/usr/bin/env python

from locust import Locust
from util import *
from tasks.HTTPRPCClient import HTTPRPCClient
from ethjsonrpc import EthJsonRpc

# Initialise function
class EthLocust(Locust):
    '''
    This is the abstract Locust class which should be subclassed.
    It provides an Ethereum JSON-RPC client that can be used for
    requests that will be tracked in Locust's statistics.
    '''
    def __init__(self, *args, **kwargs):
        super(EthLocust, self).__init__(*args, **kwargs)
        server, port = self.host.split(':')
        if int(port) == 443:
            tls_flag = True
        else:
            tls_flag = False
        self.client = EthJsonRpc(server, port, tls=tls_flag)


class EthUser(EthLocust):
    host = 'localhost:8545'
    min_wait = 10
    max_wait = 12
    task_set = HTTPRPCClient


