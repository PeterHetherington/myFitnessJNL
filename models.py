from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

db = SQLAlchemy()

# User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    workouts = db.relationship('Workout', backref='user', lazy=True, cascade="all, delete-orphan")
    sessions = db.relationship('TrainingSession', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return 'User ' + str(self.id)

# Exercise type model
class ExerciseType(db.Model):
    __tablename__ = 'exercise_type'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False, unique=True)

    # exercises = relationship('Exercise', backref='exercise_type', lazy=True)
    exercises = db.relationship('Exercise',secondary='exercise_exercise_type', back_populates='types')

    def __repr__(self):
        return 'ExerciseType ' + str(self.id) + ' ' + str(self.type) 

# Exercises model
class Exercise(db.Model):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    # type = db.Column(db.Integer, db.ForeignKey('exercise_type.id'), nullable=False)

    types = db.relationship('ExerciseType', secondary='exercise_exercise_type', back_populates='exercises')

    workout_exercises = db.relationship('WorkoutExercise', backref='exercise', lazy=True, cascade="all, delete-orphan")
    # logbooks = db.relationship('Logbook', backref='exercise', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return 'Exercise ' + str(self.id) + ' ' + str(self.name)

# Exercise type join
class ExerciseExerciseType(db.Model):
    __tablename__ = 'exercise_exercise_type'
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('exercise_type.id'), primary_key=True)
    
    def __repr__(self):
        return 'ExerciseExerciseType ' + str(self.exercise_id) + ',' + str(self.type_id)

# Workout type model
class WorkoutType(db.Model):
    __tablename__ = 'workout_type'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False, unique=True)

    workouts = db.relationship('Workout', backref='workout_type', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return 'WorkoutType ' + str(self.id) + ' ' + str(self.type)

# Workouts model
class Workout(db.Model):
    __tablename__ = 'workout'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('workout_type.id'), nullable=False)

    workout_exercises = db.relationship('WorkoutExercise', backref='workout', lazy=True, cascade="all, delete-orphan")
    sessions = db.relationship('TrainingSession', back_populates='workout', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return 'Workout ' + str(self.id)
    
# Workout Exercise model
class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercise'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'WorkoutExercise ' + str(self.id)

# Training Session model
class TrainingSession(db.Model):
    __tablename__ = 'training_session'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=True)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    workout = db.relationship('Workout', back_populates='sessions')
    logbooks = db.relationship('Logbook', backref='training_session', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return 'TrainingSession ' + str(self.id)

# Logbooks model
class Logbook(db.Model):
    __tablename__ = 'logbook'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('training_session.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False) 

    sets = db.relationship('Set', backref='logbook', lazy=True, cascade="all, delete-orphan") 
    exercise = db.relationship('Exercise', backref='logbooks')

    def __repr__(self):
        return 'Logbook ' + str(self.id) 

# Sets model
class Set(db.Model):
    __tablename__ = 'set'
    id = db.Column(db.Integer, primary_key=True)
    logbook_id = db.Column(db.Integer, db.ForeignKey('logbook.id'), nullable=False)
    set_number = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'Set ' + str(self.id)
    
# Stats model
class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # heaviest_set = db.Column(db.Integer, db.ForeignKey('set.id'))
    workouts_completed = db.Column(db.Integer, nullable=False, default=0)
    workouts_created = db.Column(db.Integer, nullable=False, default=0)
    squat_pr = db.Column(db.Integer)
    bench_pr = db.Column(db.Integer)
    deadlift_pr = db.Column(db.Integer)

    def __repr__(self):
        return 'Stats ' + str(self.id)