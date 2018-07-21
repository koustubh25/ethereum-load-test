from locust import TaskSet, task
from util import *
import random
import pprint


class HTTPRPCClient(TaskSet):

    #Private member functions
    #########################################################################

    def __get_random_block(self):
        random_block_number = random.randint(1, self.get_block_number())
        random_block = self.client.eth_getBlockByNumber(random_block_number)
        return random_block_number, random_block

    def __get_random_transaction_number_within_block(self, block_number):
        transaction_count = self.client.eth_getBlockTransactionCountByNumber(block_number)
        if transaction_count > 0 :
                return True, random.randint(1,transaction_count)
        return False, ""        

    def __get_random_transaction_within_block(self, block_number):
        transactions, transaction_number = self.__get_random_transaction_number_within_block(block_number)
        if transactions:
            return True, transaction_number
        return False, ""    
    ############################################################################

    # Tasks follow    

    # @geth_locust_task
    # @task(1)
    # def get_eth_coinbase(self):
    #     return self.client.eth_coinbase()   

    @geth_locust_task
    @task(1)
    def get_balance(self, count=10):
        addrs = []
        block = self.client.eth_getBlockByNumber()
        while len(addrs) < count:
            if block['transactions'] is not None:
                    addrs += [
                        t['to']
                        for t in block['transactions']
                        if t['to'] is not None
                    ]
        target_addr = random.choice(list(set(addrs)))
        bal = self.client.eth_getBalance(target_addr)
        return bal


    # @geth_locust_task
    # @task(10)
    def get_block_number(self):
        return self.client.eth_blockNumber()


    @geth_locust_task
    @task(1)
    def get_eth_hashrate(self):
        if(self.client.eth_mining):
            return self.client.eth_hashrate()  
          

    # @geth_locust_task
    # @task(1)
    # def get_block_transaction_count_by_hash_scaled(self):
    #     for x in range(self.number_of_blocks_to_traverse):
    #         random_block_number, random_block = self.__get_random_block()
    #         random_hash = random_block['hash']
    #         result = self.client.eth_getBlockTransactionCountByHash(random_hash)

    # returns false if blockchain is in sync
    @geth_locust_task
    @task(1)
    def is_syncing(self):
        if self.client.eth_syncing():
            raise Exception("Blockchain not in sync") 

        

    @geth_locust_task
    @task(1)
    def get_block_transaction_count_by_hash(self):
        random_block_number, random_block = self.__get_random_block()
        random_hash = random_block['hash']
        result = self.client.eth_getBlockTransactionCountByHash(random_hash)        

    # Traverse random blocks and get transaction count. Tests Disk IOPS
    # @geth_locust_task
    # @task(1)
    # def get_block_transaction_count_by_number_scaled(self):    
    #     for x in range(self.number_of_blocks_to_traverse):
    #         random_block_number, random_block = self.__get_random_block()
    #         result = self.client.eth_getBlockTransactionCountByNumber(random_block_number)

    @geth_locust_task
    @task(1)
    def get_block_transaction_count_by_number(self):    
        random_block_number, random_block = self.__get_random_block()
        result = self.client.eth_getBlockTransactionCountByNumber(random_block_number)            

    @geth_locust_task
    @task(1)
    def get_transaction_by_block_number_and_index(self):
        random_block_number, random_block = self.__get_random_block()
        transaction_count = self.client.eth_getBlockTransactionCountByNumber(random_block_number)
        if transaction_count > 0 :
            random_transaction_number = random.randint(0,transaction_count)
            self.client.eth_getTransactionByBlockNumberAndIndex(random_block_number, random_transaction_number)

    # @geth_locust_task
    # @task(1)
    # def get_transaction_by_block_number_and_index_scaled(self):
    #     for x in range(self.number_of_blocks_to_traverse):
    #         random_block_number, random_block = self.__get_random_block()
    #         transaction_count = self.client.eth_getBlockTransactionCountByNumber(random_block_number)
    #         if transaction_count > 0 :
    #             random_transaction_number = random.randint(1,transaction_count)
    #             self.client.eth_getTransactionByBlockNumberAndIndex(random_block_number, random_transaction_number)            

    @geth_locust_task
    @task(1)
    def get_uncle_by_block_hash_and_index(self):
        random_block_number, random_block = self.__get_random_block()
        for x in ['earliest', 'latest', 'pending', random_block_number]:
            transactions, transaction_number = self.__get_random_transaction_number_within_block(x)
            if transactions:
                self.client.eth_getUncleByBlockNumberAndIndex(x, transaction_number)

    # This function applies to stored contract
    # @geth_locust_task
    # @task(1)
    # def get_storage_at(self):
    #     random_block_number, random_block = self.__get_random_block()
    #     self.client.eth_getStorageAt(random_block['hash'], random_block_number)

    @geth_locust_task
    @task(1)
    def get_eth_get_uncle_count_by_block_number(self):
        random_block_number, random_block = self.__get_random_block()
        self.client.eth_getUncleCountByBlockNumber(random_block_number)

    @geth_locust_task
    @task(1)
    def eth_get_uncle_count_by_block_hash(self):
        random_block_number, random_block = self.__get_random_block()
        self.client.eth_getUncleCountByBlockHash(random_block['hash'])

    @geth_locust_task
    @task(1)
    def eth_get_uncle_by_block_hash_and_index(self):
        random_block_number, random_block = self.__get_random_block()
        transactions, transaction_number = self.__get_random_transaction_number_within_block(random_block_number)
        if transactions:
            self.client.eth_getUncleByBlockHashAndIndex(random_block['hash'], random_block_number)


    @geth_locust_task
    @task(1)
    def eth_get_transaction_receipt_by_blockhash_and_index(self):
        random_block_number, random_block = self.__get_random_block()
        transactions, transaction = self.__get_random_transaction_within_block(random_block_number)
        if transactions:
            transaction = self.client.eth_getTransactionByBlockHashAndIndex(random_block['hash'], transaction - 1)
            self.client.eth_getTransactionReceipt(transaction['hash'])