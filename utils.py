import requests


def get_request(url):
    response = requests.get(url)
    return response.json()



