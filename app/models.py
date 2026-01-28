from . import db


class Story(db.Model):
    __tablename__ = "stories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(20), default="draft")

    def to_dict(self):
        return {"id": self.id, "title": self.title, "status": self.status}
