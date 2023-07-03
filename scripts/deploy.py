from brownie import Coin, accounts
from web3 import Web3, Account




def main():
    web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

    print(web3.isConnected())

                # Inserisci la tua chiave privata MetaMask
    private_key = '3fc8d6c1f93759f3f8c2bc4b196284cb5c4e90bc2f465b5ea044561a439a11c9'

    # Aggiungi l'account admin utilizzando la chiave privata
    admin = accounts.add(private_key)
    # Inizializza il provider Web3 con MetaMask





    # Deploy del contratto Coin con saldo iniziale di 100
    coin = Coin.deploy(100, {'from': admin})

    # Ottieni l'indirizzo dell'account recipient
    recipient_address = accounts[1]

    # Esegui la trasferimento di 10 token dal admin all'account recipient
    transfer_transaction = coin.transfer(recipient_address, 10, {'from': admin})

    # Ottieni il nuovo saldo dell'account recipient
    updated_balance = coin.balanceOf(recipient_address)

    # Ottieni il nuovo saldo dell'account admin
    updated_balance2 = coin.balanceOf(admin)

    # Stampa i nuovi saldi
    print(f"Trasferimento token {recipient_address}: {updated_balance}")
    print(f"Trasferimento token {admin}: {updated_balance2}")

    # Ottenere il nonce dell'account admin
    nonce = web3.eth.getTransactionCount(admin.address)

    # Ottenere il gas price corrente
    gas_price = web3.eth.generateGasPrice()

    # Creazione dell'oggetto della transazione
    transaction = {
        'from': admin.address,
        'to': coin.address,
        'value': 0,
        'data': transfer_transaction.input,
        'gas': transfer_transaction.gas_limit,
        'gasPrice': 20000000000,
        'nonce': nonce
    }

    # Firma della transazione utilizzando la chiave privata MetaMask
    signed_txn = web3.eth.account.signTransaction(transaction, private_key)

    # Invio della transazione firmata
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    # Attendere la conferma della transazione
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)


    # Stampa l'hash della transazione confermata
    print(f"Transazione confermata: {tx_receipt['transactionHash'].hex()}")





if __name__ == '__main__':
    main()