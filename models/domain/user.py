class User:
    def __init__(self, name: str, mail: str, hash_password:str, is_admin: bool, user_id: int|None = None):
        self.name = name
        self.user_id = user_id
        self.mail = mail
        self.hash_password = hash_password
        self.is_admin = is_admin