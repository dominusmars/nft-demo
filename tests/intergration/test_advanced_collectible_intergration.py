from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_DEPLOYMENTS,
    get_account,
    get_contract,
)
import pytest
import time
from brownie import network, AdvancedCollectible
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_advanced_collectible_intergration():
    if network.show_active() in LOCAL_BLOCKCHAIN_DEPLOYMENTS:
        pytest.skip()
    account = get_account()
    advanced_collectible, creating_tx = deploy_and_create()
    time.sleep(60)
    assert advanced_collectible.tokenCounter() == 1
