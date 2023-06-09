import requests


def get_request(url: str) -> dict:
    """
    Функция для запроса к API в которую передается строка с адресом в качестве аргумента
    и возвращается словарь с ответом API.
    """
    response = requests.get(url)
    return response.json()



