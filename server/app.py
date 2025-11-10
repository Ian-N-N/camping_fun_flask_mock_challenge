import os
from flask import Flask, request, jsonify, abort, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# default to sqlite db file in server directory if no DB URL provided
db_url = os.getenv("DATABASE_URL", "sqlite:///camp.db")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# import models after db is created to avoid circular imports
from models import Camper, Activity, Signup  

# Helpers / Serializers
def camper_brief_dict(camper: Camper):
    return {"id": camper.id, "name": camper.name, "age": camper.age}

def activity_brief_dict(activity: Activity):
    return {"id": activity.id, "name": activity.name, "difficulty": activity.difficulty}

def signup_to_dict(signup: Signup):
    return {
        "id": signup.id,
        "camper_id": signup.camper_id,
        "activity_id": signup.activity_id,
        "time": signup.time,
        "activity": activity_brief_dict(signup.activity),
        "camper": camper_brief_dict(signup.camper),
    }

# Routes: Campers
@app.route("/campers", methods=["GET"])
def campers_index():
    campers = Camper.query.all()
    return jsonify([camper_brief_dict(c) for c in campers]), 200

@app.route("/campers/<int:id>", methods=["GET"])
def campers_show(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    # include signups, each signup nests activity
    signups = []
    for s in camper.signups:
        signups.append({
            "id": s.id,
            "camper_id": s.camper_id,
            "activity_id": s.activity_id,
            "time": s.time,
            "activity": activity_brief_dict(s.activity),
        })
    result = {"id": camper.id, "name": camper.name, "age": camper.age, "signups": signups}
    return jsonify(result), 200

@app.route("/campers", methods=["POST"])
def campers_create():
    data = request.get_json() or {}
    name = data.get("name")
    age = data.get("age")

    errors = []
    if not name or not str(name).strip():
        errors.append("Name is required")
    try:
        age_int = int(age)
    except Exception:
        errors.append("Age must be an integer between 8 and 18")
    else:
        if not (8 <= age_int <= 18):
            errors.append("Age must be an integer between 8 and 18")

    if errors:
        return jsonify({"errors": errors}), 400

    camper = Camper(name=name.strip(), age=age_int)
    db.session.add(camper)
    db.session.commit()
    return jsonify(camper_brief_dict(camper)), 201

@app.route("/campers/<int:id>", methods=["PATCH"])
def campers_update(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404

    data = request.get_json() or {}
    name = data.get("name", camper.name)
    age = data.get("age", camper.age)

    errors = []
    if not name or not str(name).strip():
        errors.append("Name is required")
    try:
        age_int = int(age)
    except Exception:
        errors.append("Age must be an integer between 8 and 18")
    else:
        if not (8 <= age_int <= 18):
            errors.append("Age must be an integer between 8 and 18")

    if errors:
        return jsonify({"errors": errors}), 400

    camper.name = name.strip()
    camper.age = age_int
    db.session.commit()
    return jsonify(camper_brief_dict(camper)), 202

# Routes: Activities
@app.route("/activities", methods=["GET"])
def activities_index():
    activities = Activity.query.all()
    return jsonify([activity_brief_dict(a) for a in activities]), 200

@app.route("/activities/<int:id>", methods=["DELETE"])
def activities_delete(id):
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404
    db.session.delete(activity)
    db.session.commit()
    return ("", 204)

# Routes: Signups
@app.route("/signups", methods=["POST"])
def signups_create():
    data = request.get_json() or {}
    camper_id = data.get("camper_id")
    activity_id = data.get("activity_id")
    time = data.get("time")

    errors = []

    # validate existence of camper and activity
    camper = Camper.query.get(camper_id)
    if not camper:
        errors.append("Camper must exist")
    activity = Activity.query.get(activity_id)
    if not activity:
        errors.append("Activity must exist")

    # validate time
    try:
        time_int = int(time)
    except Exception:
        errors.append("Time must be an integer between 0 and 23")
    else:
        if not (0 <= time_int <= 23):
            errors.append("Time must be an integer between 0 and 23")

    if errors:
        return jsonify({"errors": errors}), 400

    signup = Signup(camper_id=camper.id, activity_id=activity.id, time=time_int)
    db.session.add(signup)
    db.session.commit()

    # Return signup with nested activity & camper per spec
    result = {
        "id": signup.id,
        "camper_id": signup.camper_id,
        "activity_id": signup.activity_id,
        "time": signup.time,
        "activity": activity_brief_dict(signup.activity),
        "camper": {"id": camper.id, "name": camper.name, "age": camper.age}
    }
    return jsonify(result), 201

# Error handler
@app.errorhandler(400)
def handle_400(err):
    if isinstance(err.description, dict):
        return jsonify(err.description), 400
    return jsonify({"errors": ["Bad request"]}), 400

@app.errorhandler(404)
def handle_404(err):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(port=5555, debug=True)
