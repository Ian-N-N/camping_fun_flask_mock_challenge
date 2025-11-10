from app import db

class Camper(db.Model):
    __tablename__ = "campers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # one-to-many to signups
    signups = db.relationship("Signup", back_populates="camper", cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<Camper {self.id} {self.name}>"

class Activity(db.Model):
    __tablename__ = "activities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    # signups cascade on delete
    signups = db.relationship("Signup", back_populates="activity", cascade="all, delete-orphan", passive_deletes=True, lazy=True)

    def __repr__(self):
        return f"<Activity {self.id} {self.name}>"

class Signup(db.Model):
    __tablename__ = "signups"
    id = db.Column(db.Integer, primary_key=True)
    camper_id = db.Column(db.Integer, db.ForeignKey("campers.id", ondelete="CASCADE"), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    time = db.Column(db.Integer, nullable=False)

    camper = db.relationship("Camper", back_populates="signups", lazy=True)
    activity = db.relationship("Activity", back_populates="signups", lazy=True)

    def __repr__(self):
        return f"<Signup {self.id} camper:{self.camper_id} activity:{self.activity_id} time:{self.time}>"
