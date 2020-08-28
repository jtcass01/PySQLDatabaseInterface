from json import load
from os import getcwd, sep
from utilities.Logger import Logger
from typing import Union
from enum import Enum
import mariadb
import mysql.connector


class Database(object):
    def __init__(self, database_description_file_path: str, sql_type: Enum) -> None:
        with open(file=database_description_file_path) as database_description_file:
            database_description = load(fp=database_description_file)
        self.user = database_description['user']
        self.password = database_description['password']
        self.host = database_description['host']
        self.port = database_description['port']
        self.database = database_description['database']
        self.sql_type = sql_type

    def create_connection(self) -> Union[mariadb.connection, mysql.connector.connection.MySQLConnection]:
        return self.sql_type.value.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )

    def create_table(self, table_name: str, attribute_dictionary: dict) -> None:
        # Generate SQL Statement
        sql_statement = "CREATE TABLE {}(\n".format((table_name))
        for attribute_enumeration, (attribute_key, attribute_type) in enumerate(attribute_dictionary.items()):
            if attribute_enumeration == 0:
                sql_statement += attribute_key + " " + attribute_type + " PRIMARY KEY,\n"
            elif attribute_enumeration == len(attribute_dictionary.keys()) - 1:
                sql_statement += attribute_key + " " + attribute_type + ");\n"
            else:
                sql_statement += attribute_key + " " + attribute_type + ",\n"

        connection = self.create_connection()
        connection.close()

    def list_tables(self) -> Union[str, None]:
        return self.execute_query(query="SHOW TABLES;")

    def list_entries_in_table(self, table_name: str) -> Union[str, None]:
        return self.execute_query(query="SELECT * FROM " + table_name + ";")

    def execute_query(self, query: str) -> Union[str, None]:
        connection = self.create_connection()

        sql_cursor = connection.cursor()
        sql_cursor.execute(query)
        result = sql_cursor.fetchall()

        connection.close()

        return result

    def connection_test(self) -> bool:
        try:
            test_connection = self.create_connection()
            Logger.console_log(message="Connection test with " + self.database + " located at " + self.host
                                       + " was a success",
                               status=Logger.LogStatus.SUCCESS)
            return True
        except self.sql_type.value.Error as err:
            Logger.console_log(message="Unable to establish connection with database " + self.database + ". Error ["
                                       + str(err) + "] was returned",
                               status=Logger.LogStatus.FAIL)
            return False

    class SQLTypes(Enum):
        MARIA_DB = mariadb
        MYSQL = mysql.connector


if __name__ == "__main__":
    test_db = Database(database_description_file_path=getcwd() + sep + "DatabaseKeys" + sep + "JacobCassadyDotCom.json",
                       sql_type=Database.SQLTypes.MYSQL)
    test_db.connection_test()
    print(test_db.execute_query(query="SELECT school FROM TRANSCRIPT;"))
