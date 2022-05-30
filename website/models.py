from . import db

#User Table
class users(db.Model):
    id = db.Column("id", db.VARCHAR(255), primary_key=True, nullable=False)
    username = db.Column("username", db.VARCHAR(255), nullable=False)
    password = db.Column("password", db.VARCHAR(255), nullable=False)
    admin = db.Column("admin", db.Boolean, nullable=False)

    def __init__(self, id, username, password, admin):
        self.id = id
        self.username = username
        self.password = password
        self.admin = admin

#Cities Table
class cities(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.VARCHAR(255), nullable=False)
    
    def __init__(self, name):
        self._name = name

#Streets Table
class streets(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.VARCHAR(255), nullable=False)
    city = db.Column("city", db.VARCHAR(255), nullable=False)

    def __init__(self, name, city):
        self.name = name
        self.city = city

#Address Table
class addresses(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    streetnum = db.Column("streetnum", db.VARCHAR(255), nullable=False)
    street = db.Column("street", db.VARCHAR(255), nullable=False)
    city = db.Column("city", db.VARCHAR(255), nullable=False)

    def __init__(self, streetnum, street, city):
        self.streetnum = streetnum
        self.street = street
        self.city = city