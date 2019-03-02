from ethjsonrpc import EthJsonRpc
c = EthJsonRpc('127.0.0.1', 8545)
print(c.eth_gasPrice())
addr_list = c.eth_accounts()
print(addr_list)
print(c.eth_getBalance(addr_list[0], 'latest'))
print(c.eth_getBalance(addr_list[1], 'latest'))
print(c.eth_getTransactionCount (addr_list[0], 'latest'))
#c.eth_sendTransaction(addr_list[0], addr_list[1], 30400, c.eth_gasPrice(), 1000000, 0)
#print(c.db_putString('testDB', 'myKey', 'myString'))
#print(c.db_getString('testDB', 'myKey'))


