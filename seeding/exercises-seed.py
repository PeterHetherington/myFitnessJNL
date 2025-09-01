from app import app
from models import db, Exercise

exercises = [
    "Flat barbell bench press", # 1
    "Flat dumbbell bench press",
    "Incline barbell bench press",
    "Incline dumbbell bench press",
    "Decline barbell bench press",
    "Pec fly",
    "Deadlift", # 7
    "Barbell Row",
    "T-Bar Row",
    "Pull-Up",
    "Lat Pulldown",
    "Seated Cable Row",
    "Single-Arm Dumbbell Row",
    "Straight-Arm Pulldown",
    "Overhead Press",
    "Dumbbell Shoulder Press",
    "Lateral Raise",
    "Front Raise",
    "Reverse Fly",
    "Face Pull",
    "Cable Lateral Raise",
    "Shrug",
    "Squat", # 23
    "Front Squat",
    "Bulgarian Split Squat",
    "Leg Press",
    "Hack Squat",
    "Romanian Deadlift",
    "Lunge",
    "Barbell Hip Thrust",
    "Leg Extension",
    "Leg Curl",
    "Calf Raise",
    "Glute Bridge",
    "Kettlebell Swing",
    "Triceps Pushdown",
    "Overhead Triceps Extension",
    "Skull Crusher",
    "Barbell Curl",
    "EZ-Bar Curl",
    "Dumbbell Curl",
    "Hammer Curl",
    "Incline Dumbbell Curl",
    "Preacher Curl",
    "Cable Curl",
    "Sit-Up",
    "Crunch",
    "Leg Raise",
    "Plank",
    "Side Plank"
                 ]



with app.app_context():
    # types = ExerciseType.query.all()
    # print(types)
    for exercise in exercises:
        if not Exercise.query.filter_by(name=exercise).first():
            new_exercise = Exercise(name=exercise)
            db.session.add(new_exercise)
    db.session.commit()
    print("Seeded exercises successfully.")