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
        self.name = name

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
    image = db.Column("image", db.VARCHAR(255), nullable=False)
    meterNum = db.Column("meternum", db.VARCHAR(255), nullable=True)
    meterSize = db.Column("metersize", db.VARCHAR(255), nullable=True)
    tieOne = db.Column("tieone", db.VARCHAR(255), nullable=True)
    tieTwo = db.Column("tietwo", db.VARCHAR(255), nullable=True)
    notes = db.Column("notes", db.VARCHAR(400), nullable=True)



    def __init__(self, streetnum, street, city, meterNum, meterSize, tieOne, tieTwo, notes, image):
        self.streetnum = streetnum
        self.street = street
        self.city = city
        self.meterNum = meterNum
        self.meterSize = meterSize
        self.tieOne = tieOne
        self.tieTwo = tieTwo
        self.notes = notes
        self.image = image

#Changes Table
class changes(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    userID = db.Column("userid", db.VARCHAR(255), nullable=False)
    date = db.Column("date", db.DateTime, nullable=False)
    change = db.Column("change", db.VARCHAR(255), nullable=False)

    def __init__(self, userID, date, change):
        self.userID = userID
        self.date = date
        self.change = change