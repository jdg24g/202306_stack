"""MySQL connection."""

# Standard libraries
import os

# PyMySQL
import pymysql.cursors


class MySQLConnection:
    """Modelo de clase para la conexión a la base de datos (esquema)."""

    def __init__(self):
        """
        Constructor encargado de crear un objeto de tipo `MySQLConnection`.
        El constructor recibe el nombre de la base de datos a la que se desea
        conectar.
        
        Parámetros:
            - self: Es un referencia a la instancia de la clase.

        Retorno:
            - None: Retorna nada.
        """

        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=str(os.getenv("DB_PASSWORD")), 
            db=os.getenv("DB_NAME"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.connection = connection

    def query_db(self, query, data=None):
        """
        El método `query_db` es el encargado de ejecutar las consultas a la
        base de datos (esquema).

        Parámetros:
            - self: Es una referencia a la instancia de la clase.
            - query: Consulta SQL a la base de datos (esquema).
            - data: Datos a insertar en la consulta.

        Retorno:
            - False (bool): En caso que la consulta falle. 
        """
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
     
                executable = cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # Si la consulta es una inserción, devuelva el id de la
                    # última fila, ya que esa es la fila que acabamos de
                    # agregar.
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # Si la consulta es una selección, devuelva todo lo que se
                    # obtenga de la base de datos (esquema). El resultado será
                    # una lista de diccionarios.
                    result = cursor.fetchall()
                    return result
                else:
                    # Si la consulta no es una inserción o una selección, como
                    # una actualización o eliminación, confirme los cambios y
                    # no devuelva nada.
                    self.connection.commit()
            except Exception as e:
                # En caso de que la consulta falle, imprima el error y 
                # devuelva `False`.
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 


def connect_to_mysql():
    """
    La función la `connect_to_mysql` es la encargada de crear una instancia de
    la clase `MySQLConnection`, la cual será utilizada por el servidor.

    Retorno:
        - MySQLConnection (class): Instancia de la clase.
    """
    return MySQLConnection()
