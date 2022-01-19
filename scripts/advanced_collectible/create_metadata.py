from tkinter import TRUE
from brownie import AdvancedCollectible, network
from pathlib import Path
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
import requests
import json
import os

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    # "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    # "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
    "SHAPE": "https://ipfs.io/ipfs/QmSjpR5MeemUQjgXm6fsJ3rcYeV9iF7x2CuFpht9R1Viu9?filename=ufcqcgojqd.gif",
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectible = advanced_collectible.tokenCounter()
    print(f"there are {number_of_advanced_collectible} in this collection")
    for token_id in range(number_of_advanced_collectible):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it and try again")
        else:
            print(f"Creating: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An {breed}"
            image_file_path = "./img/" + breed.lower().replace("_", "-") + ".gif"
            if os.getenv("UPLOAD_TO_IPFS"):
                image_uri = upload_toipfs(image_file_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]
            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_TO_IPFS"):
                print("Uploading metadata")
                upload_toipfs(metadata_file_name)


def upload_toipfs(file_path):
    with Path(file_path).open("rb") as fp:
        img_bin = fp.read()
        ipfs_url = "http://127.0.0.1:5001/"
        endpoint = "api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": img_bin})
        print(response.json())
        ipfs_hash = response.json()["Hash"]
        filename = file_path.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
