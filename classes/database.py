from dotenv import load_dotenv
import os
import psycopg2

# Загружаем переменные окружения из файла .env
load_dotenv()


class DatabaseConnector:
    """
    Класс миксин для подключения к базе данных
    """
    def __init__(self):
        self.__db_address = os.getenv('DATABASE_ADDRESS')
        self.__db_name = os.getenv('DATABASE_NAME')
        self.__db_user = os.getenv('DATABASE_USER')
        self.__db_password = os.getenv('DATABASE_PASSWORD')
        self.connect = psycopg2.connect(host=self.__db_address,
                                   database=self.__db_name,
                                   user=self.__db_user,
                                   password=self.__db_password)
        self.cursor = self.connect.cursor()


class DBManager(DatabaseConnector):
    """
    Класс для работы с базой данных
    """
    def __init__(self) -> None:
        super().__init__()

    def create_tables(self) -> None:
        """
        Метод для создания необходимых для работы таблиц если они отсутствуют в базе данных
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
            id serial PRIMARY KEY NOT NULL,
            name VARCHAR(50) NOT NULL,
            description TEXT,
            city TEXT,
            url TEXT);        
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies 
            (
            id serial PRIMARY KEY NOT NULL,
            name VARCHAR(200) NOT NULL,
            company_id INTEGER REFERENCES companies(id),
            salary_min INTEGER,
            salary_max INTEGER,
            url TEXT
            );        
        """)
        self.connect.commit()

    def drop_tables(self) -> None:
        """
        Метод для удаления таблиц из базы данных
        """
        self.cursor.execute('DROP TABLE IF EXISTS vacancies')
        self.cursor.execute('DROP TABLE IF EXISTS companies')
        self.connect.commit()

    def insert_data(self, company: dict, vacancies: dict) -> None:
        """
        Метод для добавления данных в таблицы с компаниями и вакансиями.
        В качестве аргумента принимает словарь с информацией о компании и словарь с вакансиями.
        """
        self.cursor.execute(f'INSERT INTO companies (id, name, city, description, url) '
                            f'VALUES (%s, %s, %s, %s, %s)',
                            (
                                int(company['id']),
                                company['name'],
                                company['area']['name'],
                                company['description'],
                                company['alternate_url'])
                            )
        self.connect.commit()
        for item in vacancies['items']:
            salary_from = None
            salary_to = None
            if item.get('salary'):
                salary_from = item['salary']['from']
                salary_to = item['salary']['to']
            self.cursor.execute(f'INSERT INTO vacancies (name, company_id, salary_min, salary_max, url) '
                                f'VALUES (%s, %s, %s, %s, %s)',
                                (
                                    item['name'],
                                    item['employer']['id'],
                                    salary_from,
                                    salary_to,
                                    item['alternate_url'])
                                )
            self.connect.commit()

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Метод для запроса в базу данных, который возвращает количество вакансий в каждой компании.
        """
        self.cursor.execute("""
        SELECT companies.name, COUNT(vacancies.id)
        FROM companies
        JOIN vacancies ON vacancies.company_id = companies.id
        GROUP BY companies.name
        """)
        return self.cursor.fetchall()

    def get_all_vacancies(self) -> list[tuple]:
        """
        Метод для запроса в базу данных, который возвращает все вакансии
        """
        self.cursor.execute("""
        SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
        FROM vacancies
        JOIN companies on vacancies.company_id = companies.id
        """)
        return self.cursor.fetchall()

    def get_avg_salary(self) -> tuple:
        """
        Метод для запроса в базу данных, который возвращает среднюю зарплату по вакансиям
        """
        self.cursor.execute("""
        SELECT AVG(vacancies.salary_max)
        FROM vacancies
        """)
        return self.cursor.fetchone()

    def vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Метод для запроса в базу данных, который возвращает вакансии с зарплатой выше средней.
        """
        self.cursor.execute(f"""
        SELECT companies.name, vacancies.name, vacancies.salary_max, vacancies.url
        FROM vacancies
        JOIN companies on vacancies.company_id = companies.id
        WHERE vacancies.salary_max > ({self.get_avg_salary()[0]})
        """)
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """
        Метод для запроса в базу данных, который ищет и возвращает вакансии по ключевому слову
        """
        self.cursor.execute(f"""
        SELECT *
        FROM vacancies
        WHERE vacancies.name ILIKE '%{keyword}%'
        """)
        return self.cursor.fetchall()


if __name__ == '__main__':
    db = DBManager()
    db.create_tables()
    db.drop_tables()
