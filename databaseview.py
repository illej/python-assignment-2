import sqlite3
from view import View


class DatabaseView(View):
    def __init__(self, db):
        super(View, self).__init__()
        self.__db = db
        self.__connection = None
        self.__cursor = None
        self.initialise()

    def initialise(self):
        try:
            self.__connection = sqlite3.connect(self.__db)
            self.__cursor = self.__connection.cursor()
        except Exception as e:
            print(e)

    def rebuild(self):
        try:
            # create table
            self.__cursor.execute('''drop table if exists employee''')
            self.__cursor.execute('''CREATE TABLE IF NOT EXISTS employee
                                 (id char(4) PRIMARY KEY NOT NULL,
                                 gender char(1),
                                 age INT(2),
                                 sales INT,
                                 bmi VARCHAR(11),
                                 salary INT,
                                 birthday DATE )''')
            self.__connection.commit()
            print('-- db dropped')
            print('-- db rebuit')
        except Exception as e:
            print(e)

    def set(self, data_list):
        try:
            sql = "INSERT INTO employee (" \
                  "'id'," \
                  "'gender'," \
                  "'age'," \
                  "'sales'," \
                  "'bmi'," \
                  "'salary'," \
                  "'birthday')" \
                  "VALUES (" \
                  "'{empid}'," \
                  "'{gender}'," \
                  "'{age}'," \
                  "'{sales}'," \
                  "'{bmi}'," \
                  "'{salary}'," \
                  "'{birthday}')".format(**data_list)
            self.__cursor.execute(sql)
            self.__connection.commit()
        except Exception as e:
            # print('insert error:', e)
            pass

    def get(self, column):
        all_rows = []
        try:
            sql = "select {} from employee".format(column)
            for row in self.__cursor.execute(sql):
                all_rows.append(row)
            return all_rows
        except Exception as e:
            print(e)
