from database import db

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    value = db.Column(db.Float())
    paid = db.Column(db.Boolean)
    due_date = db.Column(db.Date())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))