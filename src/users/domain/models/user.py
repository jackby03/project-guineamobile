class User:

    def __init__(self, id: str, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"

    def as_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}
