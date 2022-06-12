import sqlite3

def readSqliteTable():
    try:
        sqliteConnection = sqlite3.connect('../instance/flaskr.sqlite')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from pedidos"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total filas son:  ", len(records))
        print("Imprimiendo filas")
        for row in records:
            print(row[0])
            print(row[1])
            print(row[2])
            print(row[3])
            print(row[4])
        # for row in records:
        #     print("Id: ", row[0])
        #     print("Name: ", row[1])
        #     print("Email: ", row[2])
        #     print("JoiningDate: ", row[3])
        #     print("Salary: ", row[4])
        #     print("\n")

        cursor.close()

    except sqlite3.Error as error:
        print("Error al leer los datos de la db", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Conexion cerrada")

readSqliteTable()
