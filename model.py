from app import *


class Queries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(12),nullable = False)
    email = db.Column(db.String(50), nullable=False, unique = True)
    inquiry = db.Column(db.String(200), nullable=False)
    reply = db.Column(db.String(200),nullable=True)
    
    
    def __repr__(self):
        return f"Queries('{self.name}','{self.number}','{self.email}',{self.inquiry})"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email =db.Column(db.String(50), nullable=False,unique=True)
    password = db.Column(db.String(20),nullable=False,unique=True)
    
    def __repr__(self):
        return f"User('{self.email}','{self.password}')"