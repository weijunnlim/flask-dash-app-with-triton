class User:
    _users = {}

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        User._users[id] = self
        User._users[username] = self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @classmethod
    def get(cls, identifier):
        return cls._users.get(identifier)

    @classmethod
    def get_by_username(cls, username):
        return cls._users.get(username)


User('1', 'hello', 'world') #id, username, pw
User('24', 'weijun', 'weijun123')

