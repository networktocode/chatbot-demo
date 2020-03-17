import requests

def get_subnet_info(subnet=None)
    url = "https://subnet.im/{subnet}"
    return requests.get(url)

