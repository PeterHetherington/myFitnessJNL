from app import app
from models import db, ExerciseType

exercise_types = [
    'Chest', 
    'Back', 
    'Shoulders', 
    'Biceps',
    'Triceps', 
    'Hamstrings', 
    'Quads', 
    'Calves',
    'Glutes',  
    'Core', 
    'Full Body', 
    'Push', 
    'Pull',
    'Legs' 
                 ]

with app.app_context():
    for exercise in exercise_types:
        if not ExerciseType.query.filter_by(type=exercise).first():
            new_type = ExerciseType(type=exercise)
            db.session.add(new_type)
    db.session.commit()
    print("Seeded exercise types successfully.")