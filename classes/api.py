import requests as req
from database import DBManager


class HeadHunterAPI:
    """
    Класс для взаимодействия с API HeadHunter
    """
    vacancies = []
    url = "https://api.hh.ru/vacancies"
    response = None

    def __init__(self) -> None:
        self.response = None

    def get_vacancies(self, keyword: str) -> None:
        """
        Метод для получения списка вакансий
        :param keyword: Ключевое слово для поиска вакансий
        """
        params = {
            'text': keyword,
            'area': 113,
            'per_page': 100,
            'only_with_salary': True,
            'search_field': 'name',
            'page': 0,
        }
        self.response = req.get(self.url, params)
        self.response.content.decode()
        self.vacancies.extend(self.response.json().get('items'))
        if self.response.json().get('pages') > 1:
            for page in range(1, self.response.json().get('pages')):
                response = req.get(f'https://api.hh.ru/vacancies?area=113&text={keyword}&per_page=100&page={page}')
                response.content.decode()
                self.vacancies.extend(response.json().get('items'))

    def add_vacancies(self):
        for vacancy in self.vacancies:
            DBManager(vacancy)
