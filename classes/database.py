from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()


class DatabaseConnector:
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
    Класс миксин для подключения к базе данных
    """
    def __init__(self) -> None:
        super().__init__()

    def create_tables(self):
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

    def drop_tables(self):
        self.cursor.execute('DROP TABLE IF EXISTS vacancies')
        self.cursor.execute('DROP TABLE IF EXISTS companies')
        self.connect.commit()

    def insert_data(self, company, vacancies):
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

    #
    # def __str__(self) -> str:
    #     return f'{self.title}\n{self.salary_from}\n{self.salary_to}\n{self.currency}'
    #
    # @classmethod
    # def insert_data(cls) -> None:
    #     """
    #     Метод класса для записи полученных вакансий в базу данных
    #     """
    #     for vacancy in cls.all_vacancies:
    #         cls.cursor.execute(f"SELECT * FROM vacancies WHERE title = '{vacancy.title}' AND "
    #                            f"requirement = '{vacancy.requirement}'")
    #         result = cls.cursor.fetchone()
    #         if not result:
    #             cls.cursor.execute('INSERT INTO vacancies (platform, vacancy_id, title, requirement, responsibility,'
    #                                'employer, salary_from, salary_to, currency, url) VALUES (?,?,?,?,?,?,?,?,?,?)',
    #                                (vacancy.platform, vacancy.vacancy_id, vacancy.title, vacancy.requirement,
    #                                 vacancy.responsibility, vacancy.employer, vacancy.salary_from, vacancy.salary_to,
    #                                 vacancy.currency, vacancy.url))
    #             cls.connect.commit()
    #
    # @classmethod
    # def delete_from_db(cls) -> None:
    #     """Удаление результата работы метода insert_data"""
    #     for vacancy in cls.all_vacancies:
    #         cls.cursor.execute(f"DELETE FROM vacancies WHERE vacancy_id = '{vacancy.vacancy_id}'")
    #         cls.connect.commit()


if __name__ == '__main__':
    db = DBManager()
    db.create_tables()
    db.drop_tables()
