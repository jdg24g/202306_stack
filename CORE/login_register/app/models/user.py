from app.config.mysql_connection import connect_to_mysql

class User:

    """
    Representa un usuario en el sistema.

    Attributes:
        id (int): El identificador único del usuario.
        first_name (str): El nombre del usuario.
        last_name (str): El apellido del usuario.
        email (str): La dirección de correo electrónico del usuario.
        password (str): La contraseña del usuario.
        created_at (str): Fecha y hora de creación del usuario.
        updated_at (str): Fecha y hora de la última actualización del usuario.

    Methods:
        get_all(): Recupera todos los usuarios almacenados en la base de datos.
            Returns:
                list[User] | False: Una lista de objetos User si se encuentran usuarios,
                o False si ocurre un error.
        
        save_user(data: dict): Guarda un nuevo usuario en la base de datos.
            Args:
                data (dict): Un diccionario con los datos del usuario a guardar.
            Returns:
                bool: True si el usuario se guardó exitosamente, False si ocurre un error.
        
        get_by_email(data: dict): Recupera un usuario por su dirección de correo electrónico.
            Args:
                data (dict): Un diccionario con la dirección de correo electrónico del usuario.
            Returns:
                User | False: Un objeto User si se encuentra el usuario, o False si ocurre un error.
    """
    def __init__(self,data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):

        """
        Recupera todos los usuarios almacenados en la base de datos.
        
        Returns:
            list[User] | False: Una lista de objetos User si se encuentran usuarios,
            o False si ocurre un error al acceder a la base de datos.
        """


        query = "SELECT * FROM users;"
        try:
            results = connect_to_mysql().query_db(query)
            users = []
            for user in results:
                users.append(cls(user))
                return users
        except:
            print(f'Ocurrio un error al obtener los usuarios utilizando {query}')
            return False
    
    @classmethod
    def save_user(cls,data:dict):

        """
        Guarda un nuevo usuario en la base de datos.

        Args:
            data (dict): Un diccionario con los datos del usuario a guardar, incluyendo:
                - 'first_name': Nombre del usuario.
                - 'last_name': Apellido del usuario.
                - 'email': Dirección de correo electrónico del usuario.
                - 'password': Contraseña del usuario.

        Returns:
            bool: True si el usuario se guardó exitosamente, False si ocurre un error al acceder a la base de datos.
        """


        query = """
                INSERT INTO users (first_name,last_name,email,password)
                VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
                """
        dato = query
        try:
            print(f'Query: {dato}')
            connect_to_mysql().query_db(query,data)
            return True
        except:
            print(f'Query: {dato}')
            print(f'Ocurrio un error al guardar el usuario utilizando {query}')
            return False

    @classmethod
    def get_by_email(cls,data:dict):
        datos = data
        query = """
                SELECT * FROM users WHERE email = %(email)s;
                """
        resultado = connect_to_mysql().query_db(query, data)
        
        print(f'Query: {query}')
        if resultado:
            return cls(resultado[0])
        return None
    