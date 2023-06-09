from classes.database import DBManager
from utils import get_request


def main():
    db = DBManager()
    db.create_tables()
    companies_ids = [1740, 15478, 2180, 64174, 84585, 1057, 3776, 1122462, 2136954, 3590333]
    for company in companies_ids:
        company_url = f'https://api.hh.ru/employers/{company}'
        vacancies_url = f'https://api.hh.ru/vacancies?employer_id={company}&per_page=100'
        company_data = get_request(company_url)
        vacancies_data = get_request(vacancies_url)
        db.insert_data(company_data, vacancies_data)


if __name__ == '__main__':
    main()
