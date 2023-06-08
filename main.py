from classes.database import DBManager
from utils import get_request


def main():
    companies_ids = [1740, 15478, 2180, 64174, 84585, 1057, 3776, 1122462, 2136954, 3590333]
    db = DBManager()
    db.create_tables()

    for company in companies_ids:
        url = f'https://api.hh.ru/vacancies?employer_id={company}'
        data = get_request(url)


if __name__ == '__main__':
    main()
