from app.config.mysqlconnection import connect_to_mysql

class User:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        
        result = connect_to_mysql().query_db(query,data)

        if result:
            return cls(result[0])
        return None
    
    @classmethod
    def create(cls,data):
        query = """
                INSERT INTO users (first_name,last_name,email,password)
                VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
                """
        return connect_to_mysql().query_db(query,data)
    