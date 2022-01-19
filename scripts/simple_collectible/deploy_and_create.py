from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import SimpleCollectible

simple_token_uri = "https://ipfs.io/ipfs/Qmc3fTnYDcNURXGZuzKQH9zpZFnKaCeQfX4sxw9JbXSUpE?filename=ufcqcgojpd.json"


def main():
    deploy_and_create()


def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(simple_token_uri, {"from": account})
    tx.wait(1)
    print(
        f"awesome, you can see nft at https://testnets.opensea.io/assets/{simple_collectible.address}/{simple_collectible.tokenCounter() - 1}"
    )
    return simple_collectible
