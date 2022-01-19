from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed, get_account, OPENSEA_URL

metadata_dic = {
    "Pug": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "Shape": "https://ipfs.io/ipfs/QmY4HtbDB9x41S7AhaAGw8JNpP7FYS8NN8aNP84EuokeXf?filename=0-Shape.json",
}


def main():
    print(f"working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collections = advanced_collectible.tokenCounter()
    print(f"number of collections: {number_of_collections}")
    for token_id in range(number_of_collections):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"setting tokenURI of {token_id}")
            set_token_uri(token_id, advanced_collectible, metadata_dic[breed])


def set_token_uri(token_id, nft_contract, token_uri):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, token_uri, {"from": account})
    tx.wait(1)
    print(
        f"Minted you can view the nft at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
