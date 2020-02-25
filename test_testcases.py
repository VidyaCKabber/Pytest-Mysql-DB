#test_testcases.py
import pytest
import mysql.connector
from mysql.connector import Error
from pytest import mark
import connection

db = connection.Database()


# def setup_module(self):
#     print("------------setup----------------")
#     global db
#     db.connect()
#
#
# def teardown_module(self):
#     print("------------teardown----------------")
#     global db
#     db.close()

@pytest.fixture(scope="module")
def db_connect():
    print("--------------------------setup module---------------------------------")
    global db
    yield db.connect()
    db.close()
    print("--------------------------teardown module-----------------------")


@pytest.fixture(scope='class')
def cursor(db_connect):
    connect = db.connection
    res = connect.cursor()

    # get records length
    res.execute("""SELECT * FROM product_details""")
    record = res.fetchall()

    record_len = len(record)
    return [res, connect, record_len]


@mark.usefixtures("cursor")
class TestCases:
    # insert queries
    sql_ins_1 = """INSERT INTO product_details (
                    id,product_name,cost)
                    VALUES
                    ('','Redmi Note 8 pro','Rs.15,999')""";
    sql_ins_2 = """INSERT INTO product_details (
                    id,product_name,cost)
                    VALUES
                    ('','Infinx hot 8','Rs.15,999')""";

    @pytest.mark.tryfirst
    def test_create_table_if_not_exists(self, cursor):
        try:
            # Create table as per requirement
            sql = """CREATE TABLE IF NOT EXISTS product_details (
                    id INT(6) AUTO_INCREMENT PRIMARY KEY,
                    product_name VARCHAR(30) NOT NULL,
                    cost VARCHAR(30) NOT NULL
                    ) """
        except mysql.connector.Error as error:
            print("Failed to created the table".format(error))
        finally:
            cursor[0].execute(sql)

    @pytest.mark.forked
    @pytest.mark.parametrize("sql", [sql_ins_1, sql_ins_2])
    def test_insert_into_table(self, sql, cursor):
        try:
            print("records length from cursor => ", cursor[2])
            cursor[0].execute(sql)

            cursor[1].commit()

            assert cursor[0].rowcount == 1, "Inserted successfully"

        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))

    @pytest.mark.set1
    def test_list_table_data(self, cursor):
        global records
        try:
            # list table as per requirement
            cursor[0].execute("""SELECT * FROM product_details""")
            records = cursor[0].fetchall()

            for row in records:
                assert int(row[0]) >= 0
                assert row[1] != ''
                assert row[2] != 'Rs.00'

        except Error as error:
            print("Error reading data from MySQL table", error)

    @pytest.mark.set1
    def test_update_table(self, cursor):
        if cursor[2] > 0:
            try:
                print("Before updating")
                squery = """SELECT * FROM product_details WHERE id = 5"""
                cursor[0].execute(squery)
                record = cursor[0].fetchall()
                print(record)

                print("After updating")

                update_query = """UPDATE product_details SET product_name='Vivo v17 pro' WHERE id=5"""
                cursor[0].execute(update_query)
                cursor[0].execute(squery)
                record = cursor[0].fetchall()

                for row in record:
                    product_name = row[1]

                assert product_name == 'Vivo v17 pro'

            except Error as error:
                print("Error while updating table from MySQL ", error)

        else:
            print("No content in the table")

    @pytest.mark.skip(reason="Don't want to delete any data")
    def test_delete_table(self, cursor):

        if cursor[2] > 0:
            try:
                query = """SELECT * FROM product_details WHERE id = 1"""

                print("Before deleting")
                cursor[0].execute(query)
                records = cursor[0].fetchall()
                print(records)

                print("After deleting")
                del_query = """DELETE FROM product_details WHERE id = 1"""
                cursor[0].execute(del_query)
                cursor[1].commit()

                # Validating the deletion
                cursor[0].execute(query)
                records = cursor[0].fetchall()

                # Validating Response
                assert len(records) == 0, "Deleted successfully"

            except mysql.connector.Error as error:
                print("Failed to delete record from table: {}".format(error))

        else:
            print("Nothing to delete")
