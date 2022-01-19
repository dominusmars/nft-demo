from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    get_network,
    get_contract,
    fund_contract_with_link,
)
from brownie import AdvancedCollectible
from web3 import Web3

simple_token_uri = "https://ipfs.io/ipfs/Qmc3fTnYDcNURXGZuzKQH9zpZFnKaCeQfX4sxw9JbXSUpE?filename=ufcqcgojpd.json"


def main():
    deploy_and_create()


def deploy_and_create():
    account = get_account()
    print(f"Using account: {account}")
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        get_network()["key_hash"],
        Web3.toWei(get_network()["fee"], "ether"),
        {"from": account},
        publish_source=get_network()["verify"],
    )
    fund_contract_with_link(advanced_collectible.address)
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New Token has been created")
    return (advanced_collectible, creating_tx)
