from brownie import (
    accounts,
    network,
    config,
    Contract,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
)

LOCAL_BLOCKCHAIN_DEPLOYMENTS = ["development", "ganache-local"]
FOCKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
# NETWORKED = config["networks"][network.show_active()]

DECIMALS = 8
STARTING_PRICE = 200000000000

BREEDMAPPING = {0: "Pug", 1: "Shape"}


def get_breed(breedID):
    return BREEDMAPPING[breedID]


def get_network():
    return config["networks"][network.show_active()]


def get_account(index=None, id=None):

    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_DEPLOYMENTS
        or network.show_active() in FOCKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """This function will grab the contract addresses from brownie config if defined, otherwise
    it will deploy mock versions of the necessary contracts and return the mock contracts

        Args:
            contract_name(string)

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed contract
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_DEPLOYMENTS:
        if len(contract_type) <= 0:
            deploy_mock()
        contract = contract_type[-1]
    else:
        contract_address = get_network()[contract_name]

        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )

    return contract


def deploy_mock(decimals=DECIMALS, starting_price=STARTING_PRICE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, starting_price, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed Mock")


def fund_contract_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print(f"Funding sent to {contract_address}")
    return tx
