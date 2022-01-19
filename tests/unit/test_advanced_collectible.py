from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_DEPLOYMENTS,
    get_account,
    get_contract,
)
import pytest
from brownie import network, AdvancedCollectible
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collection():
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEPLOYMENTS:
        pytest.skip()
    account = get_account()
    advanced_collectible, creating_tx = deploy_and_create()
    requestId = creating_tx.events["requestedCollectable"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_collectible.address, {"from": account}
    )
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 2
