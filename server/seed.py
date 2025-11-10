from app import app, db
from models import Camper, Activity, Signup
from faker import Faker
import random

fake = Faker()

with app.app_context():
    print("Clearing existing data...")
    Signup.query.delete()
    Activity.query.delete()
    Camper.query.delete()
    db.session.commit()

    print("Seeding campers...")
    campers = []
    for _ in range(10):  # create 10 campers
        camper = Camper(
            name=fake.first_name(),
            age=random.randint(8, 18)  # random age between 8 and 18
        )
        campers.append(camper)
        db.session.add(camper)
    db.session.commit()

    print("Activities seeding...")
    activities = []
    activity_names = [
        "Archery", "Canoeing", "Hiking", "Fishing",
        "Rock Climbing", "Swimming", "Arts & Crafts",
        "Soccer", "Cooking", "Nature Walks"
    ]
    for name in activity_names:
        activity = Activity(
            name=name,
            difficulty=random.randint(1, 5)
        )
        activities.append(activity)
        db.session.add(activity)
    db.session.commit()

    print("Seeding signups...")
    for camper in campers:
        # Each camper signs up for 1–3 random activities
        chosen_activities = random.sample(activities, random.randint(1, 3))
        for activity in chosen_activities:
            signup = Signup(
                camper_id=camper.id,
                activity_id=activity.id,
                time=random.randint(8, 17)  # random time between 8 AM and 5 PM
            )
            db.session.add(signup)
    db.session.commit()

    print("Seeding complete!")
