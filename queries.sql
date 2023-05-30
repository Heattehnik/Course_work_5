--Создания таблицы работодателей
CREATE TABLE Employers (
  id serial PRIMARY KEY NOT NULL,
  hh_id int NOT NULL,
  name VARCHAR(50),
  description TEXT,
  url TEXT
);
--Создание таблицы вакансий
CREATE TABLE Vacancies (
  id serial PRIMARY KEY,
  employer_id INT,
  title VARCHAR(50),
  description TEXT,
  requirements TEXT,
  salary_from DECIMAL(10, 2),
  salary_to DECIMAL(10, 2),
  location VARCHAR(50),
  FOREIGN KEY (employer_id) REFERENCES Employers(id)
);