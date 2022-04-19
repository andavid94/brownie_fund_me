from brownie import network, accounts, exceptions
import pytest
from scripts.helper_scripts import get_account, LOCAL_BLOCKCHAIN_ENVS
from scripts.deploy import deploy_fund_me


def testCanFundAndWithdraw():
    account = get_account()
    fundMe = deploy_fund_me()
    entranceFee = fundMe.getEntranceFee() + 100

    tx = fundMe.fund({"from": account, "value": entranceFee})
    tx.wait(1)
    assert fundMe.addressToAmountFunded(account.address) == entranceFee

    tx2 = fundMe.withdraw({"from": account})
    tx2.wait(1)
    assert fundMe.addressToAmountFunded(account.address) == 0


def testOnlyOwnerCanWithdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVS:
        pytest.skip("only for local testing")

    account = get_account()
    fundMe = deploy_fund_me()
    badActor = accounts.add()
    #fundMe.withdraw({"from": badActor})
    with pytest.raises(exceptions.VirtualMachineError):
        fundMe.withdraw({"from": badActor})
