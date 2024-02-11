from web3 import Web3
import random
from web3.middleware import geth_poa_middleware
logged_in_person = 2
add_modifier,logged_in_addr,choice = "","",""
if (logged_in_person == 1):
    logged_in_addr = "0x754823e3af45f234c1759a1fbdb289b4839ec9c2"
    add_modifier = "1"
    choice = "0x8b6bd9eb9b7f9b8dc89b5e64dbee4b3c1e705e18"
elif (logged_in_person == 2):
    logged_in_addr = "0x8b6bd9eb9b7f9b8dc89b5e64dbee4b3c1e705e18"
    add_modifier = "2"
    choice = "0x754823e3af45f234c1759a1fbdb289b4839ec9c2"

data = []

w3 = Web3(Web3.IPCProvider('/home/saatvik/Downloads/geth-alltools-linux-amd64-1.13.12-02eb36af/node'+ add_modifier+'/geth.ipc'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# Check connection
if w3.is_connected():
    print("Connected to Geth!")
else:
    print("Failed to connect to Geth")

address = Web3.to_checksum_address(logged_in_addr)

def pay_contact(amount,reciever):
    w3.eth.send_transaction({'to':reciever,'from':address,'value':amount})
    lat_trans = {'Type':'Paid','value':amount,'to':reciever}
    data.append(lat_trans)
    return data 









choice = Web3.to_checksum_address(choice)
print(w3.eth.get_balance(w3.eth.accounts[0]))
pay_contact(12345,choice)

def trans_history(data):

    for x in range(w3.eth.block_number-1200,w3.eth.block_number):
        block = w3.eth.get_block(x,True)
        for transaction in block.transactions:
            if transaction['to'] == address or transaction['from'] == address:
                add_str = ""
                if transaction['to'] == address:
                    add_str = "Recieved: " + str(transaction['value']) + " from: " + transaction['from']
                    data.append({'Type':'Recieved','value':transaction['value'],'from':transaction['from']})
                else:
                    add_str = "Paid: " + str(transaction['value']) + " to: " + transaction['to']
                    data.append({'Type':'Paid','value':transaction['value'],'to':transaction['to']})
                print(add_str)
            else:
                print("no")
    return data

trans_history(data)
print(data)