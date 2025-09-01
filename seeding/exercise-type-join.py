from app import app
from models import db, ExerciseType, Exercise, ExerciseExerciseType

exercise_join = {
    "Chest" : [
        "Flat barbell bench press",
        "Flat dumbbell bench press",
        "Incline barbell bench press",
        "Incline dumbbell bench press",
        "Decline barbell bench press",
        "Pec fly"
    ],
    "Back" : [
        "Deadlift",
        "Barbell Row",
        "T-Bar Row",
        "Pull-Up",
        "Lat Pulldown",
        "Seated Cable Row",
        "Single-Arm Dumbbell Row",
        "Straight-Arm Pulldown"
    ],
    "Shoulders" : [
        "Overhead Press",
        "Dumbbell Shoulder Press",
        "Lateral Raise",
        "Front Raise",
        "Reverse Fly",
        "Face Pull",
        "Cable Lateral Raise",
        "Shrug"
    ],
    "Legs" : [
        "Squat",
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
        "Kettlebell Swing"
    ],
   "Triceps" : [
        "Triceps Pushdown",
        "Overhead Triceps Extension",
        "Skull Crusher"
    ],
    "Biceps" : [
        "Barbell Curl",
        "EZ-Bar Curl",
        "Dumbbell Curl",
        "Hammer Curl",
        "Incline Dumbbell Curl",
        "Preacher Curl",
        "Cable Curl"
    ],
    "Core" : [
        "Sit-Up",
        "Crunch",
        "Leg Raise",
        "Plank",
        "Side Plank"
    ]
}

with app.app_context():
    for type_name, exercises in exercise_join.items():
        exercise_type = ExerciseType.query.filter_by(type=type_name).first()
        if exercise_type:
            type_id = exercise_type.id
            for exercise_name in exercises:
                exercise = Exercise.query.filter_by(name=exercise_name).first()
                if exercise:
                    new_join = ExerciseExerciseType(exercise_id=exercise.id, type_id=type_id)
                    db.session.add(new_join)
    db.session.commit()
    print("Seeded exercise type join successfully.")