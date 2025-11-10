from flask import Flask, jsonify, request
from db import db
from models import Camper, Activity, Signup
from faker import Faker
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///camp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

fake = Faker()

# CAMPERS
@app.route("/campers", methods=["GET"])
def get_campers():
    campers = Camper.query.all()
    result = [{"id": c.id, "name": c.name, "age": c.age} for c in campers]
    return jsonify(result), 200

@app.route("/campers/<int:id>", methods=["GET"])
def get_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404

    signups_list = []
    for s in camper.signups:
        signups_list.append({
            "id": s.id,
            "camper_id": s.camper_id,
            "activity_id": s.activity_id,
            "time": s.time,
            "activity": {
                "id": s.activity.id,
                "name": s.activity.name,
                "difficulty": s.activity.difficulty
            }
        })

    return jsonify({
        "id": camper.id,
        "name": camper.name,
        "age": camper.age,
        "signups": signups_list
    }), 200

@app.route("/campers", methods=["POST"])
def create_camper():
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")

    errors = []
    if not name:
        errors.append("Name is required")
    if not isinstance(age, int) or age < 8 or age > 18:
        errors.append("Age must be an integer between 8 and 18")
    if errors:
        return jsonify({"errors": errors}), 400

    camper = Camper(name=name, age=age)
    db.session.add(camper)
    db.session.commit()
    return jsonify({"id": camper.id, "name": camper.name, "age": camper.age}), 201

@app.route("/campers/<int:id>", methods=["PATCH"])
def update_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404

    data = request.get_json()
    name = data.get("name")
    age = data.get("age")

    errors = []
    if name is not None and name.strip() == "":
        errors.append("Name cannot be empty")
    if age is not None:
        if not isinstance(age, int) or age < 8 or age > 18:
            errors.append("Age must be an integer between 8 and 18")

    if errors:
        return jsonify({"errors": errors}), 400

    if name:
        camper.name = name
    if age:
        camper.age = age
    db.session.commit()

    return jsonify({"id": camper.id, "name": camper.name, "age": camper.age}), 202

# ACTIVITIES
@app.route("/activities", methods=["GET"])
def get_activities():
    activities = Activity.query.all()
    result = [{"id": a.id, "name": a.name, "difficulty": a.difficulty} for a in activities]
    return jsonify(result), 200

@app.route("/activities/<int:id>", methods=["DELETE"])
def delete_activity(id):
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404

    db.session.delete(activity)
    db.session.commit()
    return '', 204

# SIGNUPS
@app.route("/signups", methods=["POST"])
def create_signup():
    data = request.get_json()
    camper_id = data.get("camper_id")
    activity_id = data.get("activity_id")
    time = data.get("time")

    errors = []
    camper = Camper.query.get(camper_id)
    activity = Activity.query.get(activity_id)
    if not camper:
        errors.append("Camper does not exist")
    if not activity:
        errors.append("Activity does not exist")
    if not isinstance(time, int) or time < 0 or time > 23:
        errors.append("Time must be an integer between 0 and 23")

    if errors:
        return jsonify({"errors": errors}), 400

    signup = Signup(camper_id=camper.id, activity_id=activity.id, time=time)
    db.session.add(signup)
    db.session.commit()

    return jsonify({
        "id": signup.id,
        "camper_id": camper.id,
        "activity_id": activity.id,
        "time": signup.time,
        "camper": {"id": camper.id, "name": camper.name, "age": camper.age},
        "activity": {"id": activity.id, "name": activity.name, "difficulty": activity.difficulty}
    }), 201

# SEED DATA 
@app.cli.command("seed")
def seed():
    """Seed the database with fake data."""
    from models import Camper, Activity, Signup
    db.drop_all()
    db.create_all()

    # Seed campers
    campers = []
    for _ in range(10):
        camper = Camper(name=fake.first_name(), age=random.randint(8, 18))
        campers.append(camper)
        db.session.add(camper)

    # Seed activities
    activities = []
    activity_names = [
        "Archery", "Canoeing", "Hiking", "Fishing",
        "Rock Climbing", "Swimming", "Arts & Crafts",
        "Soccer", "Cooking", "Nature Walks"
    ]
    for name in activity_names:
        activity = Activity(name=name, difficulty=random.randint(1, 5))
        activities.append(activity)
        db.session.add(activity)

    db.session.commit()

    # Seed signups
    for camper in campers:
        chosen_activities = random.sample(activities, random.randint(1, 3))
        for activity in chosen_activities:
            signup = Signup(
                camper_id=camper.id,
                activity_id=activity.id,
                time=random.randint(8, 17)
            )
            db.session.add(signup)

    db.session.commit()
    print("Database seeded with fake data!")

# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True, port=5555)
