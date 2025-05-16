from app import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id           = db.Column(db.Integer,  primary_key=True)
    name         = db.Column(db.String,   nullable=False)
    is_completed = db.Column(db.Boolean,  default=False, nullable=False)

    def to_dict(self):
        return {
            'id':           self.id,
            'name':         self.name,
            'is_completed': self.is_completed
        }
