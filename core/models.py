from core import db
from datetime import datetime, timedelta


class ShortUrls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_id = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)
    expiration_date = db.Column(
        db.DateTime(), default=datetime.now() + timedelta(minutes=15), nullable=True
    )
