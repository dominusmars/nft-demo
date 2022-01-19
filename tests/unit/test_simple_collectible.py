from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_DEPLOYMENTS, get_account
import pytest
from brownie import network
from scripts.simple_collectible.deploy_and_create import deploy_and_create

def test_can_create_simple_collectiale():
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEPLOYMENTS:
        pytest.skip()
    simple_collectiale = deploy_and_create()
    assert simple_collectiale.ownerOf(0) == get_account()