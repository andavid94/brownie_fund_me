from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3


DECIMALS = 8
STARTING_PRICE = 200000000000
FORKED_LOCAL_ENVS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVS = ["development", "ganache-local"]


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVS or network.show_active() in FORKED_LOCAL_ENVS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"the active network is {network.show_active()}")
    print("deploying mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {
                                "from": get_account()})
    #price_feed_address = MockV3Aggregator[-1].address
    print("mock deployed!")
