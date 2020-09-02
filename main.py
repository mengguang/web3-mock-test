import sys
import time

sys.modules['eth_keys.constants'] = __import__('newchain-keys-constants')

from web3.exceptions import TransactionNotFound


def main():
    from web3.auto import Web3
    from web3.middleware import geth_poa_middleware
    from eth_account.datastructures import SignedTransaction

    w3 = Web3(Web3.HTTPProvider("https://rpc1.newchain.newtonproject.org"))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    print(f'blockNumber: {w3.eth.blockNumber}')

    with open('a4d79e4efecd77ba0e1b6551388a7d7c0778824a.json') as keyfile:
        encrypted_key = keyfile.read()
        private_key = w3.eth.account.decrypt(encrypted_key, '123qwe')
        # tip: do not save the key or password anywhere, especially into a shared source file

        account = w3.eth.account.privateKeyToAccount(private_key)
        print(f'address: {account.address}')

        nonce = w3.eth.getTransactionCount(account.address)
        print(f'nonce: {nonce}')

        gas_price = w3.eth.gasPrice;
        print(f"gasPrice: {gas_price}")

        chain_id = 1007

        transaction = {
            'to': '0x29e9356eC2082f447a7F747bF8D83c35E858fb86',
            'value': w3.toWei(1, "ether"),
            'gas': 21000,
            'gasPrice': gas_price,
            'nonce': nonce,
            'chainId': chain_id
        }
        signed: SignedTransaction = w3.eth.account.sign_transaction(transaction, private_key)
        print(signed)
        # When you run sendRawTransaction, you get back the hash of the transaction:
        w3.eth.sendRawTransaction(signed.rawTransaction)
        print(f"tx hash: {w3.toHex(signed.hash)}")

        while True:
            try:
                receipt = w3.eth.getTransactionReceipt(signed.hash)
                print("transaction is confirmed.")
                print(receipt)

                break
            except TransactionNotFound:
                print("waiting for transaction to be confirmed.")
                time.sleep(3)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
