from brownie import FundMe, config, network, MockV3Aggregator
from scripts.helper_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVS,
)


def deploy_fund_me():
    account = get_account()
    # pass pricefeed address to FundMe constructor
    # if we are on a persisitent network like Rinkeby, use associated address
    # else, deploy mock
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVS:
        #price_feed_address = "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e"
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify")
    )
    print(f"contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
