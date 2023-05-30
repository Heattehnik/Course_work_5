import psycopg2
import requests


def get_employers(emp_ids: list) -> list:
    all_employers = []
    for id_ in emp_ids:
        url = f'https://api.hh.ru/employers/{id_}'
        response = requests.get(url).json()
        all_employers.append(response)
    return all_employers


def get_vacancies_by_company():
    with psycopg2.connect(host='45.141.102.19', database='headhunter', user='roman', password='2901') as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT hh_id FROM employers')
            employers = cur.fetchall()
        for company in employers:
            something = company[0]
            print(something)


def add_employers_to_db(employers_list:list) -> None:

    for employer in employers_list:
        with psycopg2.connect(host='45.141.102.19', database='headhunter', user='roman', password='2901') as conn:
            employer_id = int(employer["id"])
            with conn.cursor() as cur:
                cur.execute('CREATE TABLE IF NOT EXISTS Employers ('
                            'id serial PRIMARY KEY NOT NULL,'
                            'hh_id int UNIQUE NOT NULL,'
                            'name VARCHAR(50),'
                            'description TEXT,'
                            'url TEXT);')
                conn.commit()
                cur.execute(f'SELECT EXISTS (SELECT * FROM employers WHERE hh_id = {employer_id});')
                check_existence = cur.fetchone()
                if not check_existence[0]:
                    cur.execute('INSERT INTO employers (hh_id, name, description, url) '
                                'VALUES (%s, %s, %s, %s)',
                                (employer["id"], employer["name"], employer["description"], employer["alternate_url"]))


if __name__ == '__main__':
    top_companies = [3529, 1740, 80]
    employers = get_employers(top_companies)
    add_employers_to_db(employers)
    get_vacancies_by_company()


