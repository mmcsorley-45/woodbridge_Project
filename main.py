from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50))  # e.g. "school", "fire"

    tickets = db.relationship('Ticket', backref='location', lazy=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue = db.Column(db.String(100), nullable=False)  # ✅ renamed from 'title'
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')  # open/in_progress/closed
    assigned_to = db.Column(db.String(100))
    assigned_by = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_closed = db.Column(db.DateTime, nullable=True)

    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)