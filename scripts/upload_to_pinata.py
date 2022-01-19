import os
import requests
from pathlib import Path

PINATA_BASE_URL = "https://api.pinata.cloud/"
ENDPOINT = "pinning/pinFileToIPFS"
file_path = "./img/pug.png"
filename = file_path.split("/")[-1:][0]
headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

print(headers)


def main():
    with Path(file_path).open("rb") as fp:
        imgbin = fp.read()
        response = requests.post(
            PINATA_BASE_URL + ENDPOINT, files={"file": imgbin}, headers=headers
        )
        print(response.json())
