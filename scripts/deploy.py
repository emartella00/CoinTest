from brownie import BDT, accounts, config
from scripts.help_script import get_account
from web3 import Web3




def main():

    web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

    account = get_account()

    init_supply = Web3.toWei(10, "ether")

    coin = BDT.deploy(init_supply, {'from': account})

    print(f"CB Token Deployed all' indirizzo {coin.address}")

    receving_address = accounts[1]

    transfer_transaction = coin.transfer(receving_address, 10, {'from': account})

    updated_balance = coin.balanceOf(receving_address)

    updated_balance2 = coin.balanceOf(account)

    print(f"Trasferimento token {receving_address}: {updated_balance}")

    print(f"Trasferimento token {account}: {updated_balance2}")

    nonce = web3.eth.getTransactionCount(account.address)

    transaction = {
        'from': account.address,
        'to': coin.address,
        'value': 0,
        'data': transfer_transaction.input,
        'gas': transfer_transaction.gas_limit,
        'gasPrice': 20000000000,
        'nonce': nonce
    }

    signed_txn = web3.eth.account.sign_transaction(transaction, config["wallets"]["from_key"])

    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    print(f"Transazione confermata: {tx_receipt['transactionHash'].hex()}")


