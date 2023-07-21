import pymssql
from contextlib import contextmanager

import utils

class MSSQLBase:
    def __init__(self):
        settings = utils.get_settings()
        self.server = settings.db.server
        self.database = settings.db.db_name
        self.username = settings.db.user
        self.password = settings.db.pwd
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = pymssql.connect(server=self.server, database=self.database, user=self.username, password=self.password)
        self.cursor = self.conn.cursor()

    def query(self, query:str):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert(self, table:str, columns:list, values:tuple):
        placeholders = ', '.join(['%s'] * len(values))
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        self.cursor.execute(sql, values)
        self.conn.commit()

    def insert_by_df(self, df, table:str):
        sql = self.dataframe_to_sql_insert(df, table)
        self.cursor.execute(sql)
        self.conn.commit()

    def delete(self, table:str, condition:str):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()

    def dataframe_to_sql_insert(self, df, table:str) -> str:
        column_names = ", ".join(df.columns)
        rows = []

        for _, row in df.iterrows():
            values = ", ".join([f"'{value}'" if isinstance(value, str) else str(value) for value in row.values])
            rows.append(f"({values})")

        sql = f"INSERT INTO {table} ({column_names}) VALUES {', '.join(rows)};"
        return sql

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

# DONE: contextlib，使用@contextmanager
# TODO: 考慮使用連接池
class MSSQLBaseSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            print('DB 尚未實例化')
            cls._instance = super().__new__(cls)
            print('DB 實例化成功')
        return cls._instance

    def __init__(self):
        settings = utils.get_settings()
        self.server = settings.db.server
        self.database = settings.db.db_name
        self.username = settings.db.user
        self.password = settings.db.pwd
        self.conn = None
        self.cursor = None


    @contextmanager
    def connect(self):
        conn = pymssql.connect(server=self.server, database=self.database, user=self.username, password=self.password)
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def query(self, query:str):
        with self.connect() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def insert(self, table:str, columns:list, values:tuple):
        placeholders = ', '.join(['%s'] * len(values))
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        with self.connect() as cursor:
            cursor.execute(sql, values)

    def insert_by_df(self, df, table:str):
        sql = self.dataframe_to_sql_insert(df, table)
        with self.connect() as cursor:
            cursor.execute(sql)

    def delete(self, table:str, condition:str):
        query = f"DELETE FROM {table} WHERE {condition}"
        with self.connect() as cursor:
            cursor.execute(query)

    def dataframe_to_sql_insert(self, df, table:str) -> str:
        column_names = ", ".join(df.columns)
        rows = []

        for _, row in df.iterrows():
            values = ", ".join([f"'{value}'" if isinstance(value, str) else str(value) for value in row.values])
            rows.append(f"({values})")

        sql = f"INSERT INTO {table} ({column_names}) VALUES {', '.join(rows)};"
        return sql