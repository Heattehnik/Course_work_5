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
    count_companies_and_vacancies = db.get_companies_and_vacancies_count()

    for item in count_companies_and_vacancies:
        print(f'Компания: {item[0]}\n'
              f'Количество вакансий: {item[1]}\n')

    input('Нажмите Enter для продолжения.')

    all_vacancies = db.get_all_vacancies()

    for item in all_vacancies:
        print(f'Компания: {item[0]}\n'
              f'Название вакансии: {item[1]}\n'
              f'Зарплата от: {item[2]}\n'
              f'Зарплата до: {item[3]}\n'
              f'Ссылка на вакансию: {item[4]}\n')

    input('Нажмите Enter для продолжения.')

    avg_salary = db.get_avg_salary()
    print(f'Средняя зарплата по вакансиям составляет: {int(avg_salary[0])} руб.')

    input('Нажмите Enter для продолжения.')

    higher_salary = db.vacancies_with_higher_salary()
    print(f'Вакансии с зарплатами выше средней\n')

    for item in higher_salary:
        print(f'Компания: {item[0]}\n'
              f'Название вакансии: {item[1]}\n'
              f'Зарплата до: {item[2]}\n'
              f'Ссылка на вакансию: {item[3]}\n')

    input('Нажмите Enter для продолжения.')

    keyword = input('Введите ключевое слово для поиска:\n')
    finded_vacancies = db.get_vacancies_with_keyword(keyword)
    print('Вот что нашлось:\n')

    for item in finded_vacancies:
        print(f'Название вакансии: {item[1]}\n'
              f'Зарплата от: {item[3]}\n'
              f'Зарплата до: {item[4]}\n'
              f'Ссылка на вакансию: {item[5]}\n')


if __name__ == '__main__':
    main()
