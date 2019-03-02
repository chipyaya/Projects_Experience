# https://github.com/ethereum/web3.py
# http://web3py.readthedocs.io/en/latest

from web3 import Web3, IPCProvider

def create_acct(conn, pwd):
    return conn.personal.newAccount(pwd)

def get_balance(conn, addr):
    return conn.eth.getBalance(addr)# / Web3.toWei(1, 'ether')

def send(conn, addr1, addr2, v):
    value = Web3.toWei(v, 'ether')
    return conn.eth.sendTransaction({'from': addr1, 'to': addr2, 'value': value})

def move(conn, addr1, addr2, v):
    #TODO
    pass

def list_records(conn, addr):
    #TODO RECORD TIME
    records = []
    for i in range(conn.eth.blockNumber):
        block = conn.eth.getBlock(i)
        for trans_hash in block.transactions:
            trans = conn.eth.getTransaction(trans_hash)
            if trans.to == addr:
                records.append({'from': trans['from'], 'value': trans.value})
    return records

if __name__ == '__main__':
    conn = Web3(IPCProvider('/tmp/geth.ipc'))
    addr0 = conn.toChecksumAddress("0xa55bf47ed6211eed54981889447d755ff946cbef")

    '''
    addr1 = create_acct(conn, 'pwd')
    exchange = create_acct(conn, 'pwd')
    margin = create_acct(conn, 'pwd')
    funding = create_acct(conn, 'pwd')
    print(exchange)
    print(margin)
    print(funding)
    print(addr1)

    print('===Before===')
    print('0:', get_balance(conn, addr0))
    print('1:', get_balance(conn, addr1))
    print('e:', get_balance(conn, exchange))
    conn.personal.unlockAccount(addr0, 'pwd')
    send(conn, addr0, exchange, 10)
    
    print('===After send===')
    print('0:', get_balance(conn, addr0))
    print('1:', get_balance(conn, addr1))
    print('e:', get_balance(conn, exchange))
    move(conn, addr0, margin, 10)
    '''

    exchange = conn.toChecksumAddress('0xf857C715ed67f746722a7cA82E77300Ef365e964')
    margin = conn.toChecksumAddress('0x944C1ebCC62A3D77Ba3680419B460bB690084274')
    funding = conn.toChecksumAddress('0x4AcBCa3e0154d89a2eEf83a5A7D598805D0ed611')
    addr1 = conn.toChecksumAddress('0xbd170c525ec0d402f51163447ef73cFdB4124ac0')
    print(list_records(conn, exchange))
    print(list_records(conn, margin))
    print(list_records(conn, funding))
    print(list_records(conn, addr1))
    
    '''
    conn.personal.unlockAccount(exchange, 'pwd')
    conn.personal.unlockAccount(addr1, 'pwd')
    move(conn, addr1, funding, 1)
    print('===After===')
    print('0:', get_balance(conn, addr0))
    print('1:', get_balance(conn, addr1))
    print('e:', get_balance(conn, exchange))
    send(conn, exchange, addr1, 1)
    print('===After send===')
    print('0:', get_balance(conn, addr0))
    print('1:', get_balance(conn, addr1))
    print('e:', get_balance(conn, exchange))
    '''
