import pymssql
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

    def connect(self):
        self.conn = pymssql.connect(server=self.server, database=self.database, user=self.username, password=self.password)
        self.cursor = self.conn.cursor()

    def query(self, query:str):
        self.connect()
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.close()
        return result

    def insert(self, table:str, columns:list, values:tuple):
        self.connect()
        placeholders = ', '.join(['%s'] * len(values))
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        self.cursor.execute(sql, values)
        self.conn.commit()
        self.close()

    def insert_by_df(self, df, table:str):
        self.connect()
        sql = self.dataframe_to_sql_insert(df, table)
        self.cursor.execute(sql)
        self.conn.commit()
        self.close()

    def delete(self, table:str, condition:str):
        self.connect()
        query = f"DELETE FROM {table} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()
        self.close()

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