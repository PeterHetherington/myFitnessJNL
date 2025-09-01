from app import app
from models import db, WorkoutType

workout_types = [
    'Chest', 
    'Back', 
    'Shoulders', 
    'Legs',
    'Arms', 
    'Upper Body', 
    'Lower Body', 
    'Full Body', 
    'Push', 
    'Pull' 
                 ]

with app.app_context():
    for type in workout_types:
        if not WorkoutType.query.filter_by(type=type).first():
            new_type = WorkoutType(type=type)
            db.session.add(new_type)
    db.session.commit()
    print("Seeded workout types successfully.")