from flask import Flask, render_template, request, redirect, url_for, session, flash
from collections import defaultdict
from datetime import datetime, timedelta
from models import db, User, ExerciseType, Workout, Exercise, WorkoutType, WorkoutExercise, TrainingSession, Logbook, Set, Stats
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
app = Flask(__name__)

# configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize db with app

# secret key
app.secret_key = "FrancescoTotti23"

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # check for blank fields
        if not username or not email or not password or not confirm_password:
            flash("All fields must be filled in", category="error")
            return render_template("register.html")
        
        # check password confirmation
        if password != confirm_password:
            flash("Passwords don't match, please try again")
            return render_template("register.html")
        
        # check if user already exists
        user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if user:
            flash("Username already exists", category="error")
            return render_template("register.html")
        elif existing_email:
            flash("Email already used", category="error")
            return render_template("register.html")
        
        # hash password
        hashed_password = generate_password_hash(password)
        
        # create a new user
        new_user = User(username=username, email=email, password=hashed_password)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        
        # create a session
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # get the form data
        username = request.form['username']
        password = request.form['password']
       
        # check for blank fields
        if not username or not password:
            flash("Fields cannot be blank", category="error")
            return render_template("index.html")
       
        # check if user exists
        user = User.query.filter_by(username=username).first()
        if user:
            # check if password is correct
            if check_password_hash(user.password, password):
                # create a session
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash("Incorrect password", category="error")
                return render_template("index.html")
        else:
            flash("user doesn't exist", category="error")
            return redirect(url_for('index'))
    return render_template('index.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/workouts", methods=['GET'])
def workouts():
    # get user
    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
            flash("Please login", category="error")
            return render_template('index.html')
    
    # get users workouts
    user_workouts = Workout.query.filter_by(user_id=user.id).all()

    return render_template('workouts.html', workouts=user_workouts)

@app.route("/add-workout", methods=['POST', 'GET'])
def add_workout():
    if request.method == 'POST':
        # get user
        username = session.get('username')
        user = User.query.filter_by(username=username).first()

        if not user:
            flash("You must be signed in to create a workout", category="error")
            return render_template('index.html')
        
        # get form data
        workout_name = request.form['workout_name']
        description = request.form['description']
        workout_type = request.form['type']
        exercise_names = request.form.getlist('exercise')

        # print(workout_name)
        # print(description)
        # print(workout_type)
        # print(exercise_names)

        if not workout_name or not description or not workout_type or not exercise_names:
            flash("Fields cannot be blank", category="error")
            return render_template('add-workout.html')

        # create new workout
        new_workout = Workout(name=workout_name, description=description, user_id=user.id, type_id=workout_type)
        db.session.add(new_workout)
        db.session.commit()

        # get new workout id
        new_workout_id = new_workout.id

        # loop through exercise list
        # create new exercise in workout_exercises
        for i, exercise_name in enumerate(exercise_names, start=1):
            if exercise_name:
                exercise = Exercise.query.filter_by(name=exercise_name).first()
                if exercise:
                    new_exercise = WorkoutExercise(workout_id=new_workout_id, exercise_id=exercise.id, order=i)
                    db.session.add(new_exercise)
        db.session.commit()

         # get stats
        existing_stats = Stats.query.filter_by(user_id=user.id).first()

        if existing_stats:
            # update stats workouts_created
            existing_stats.workouts_created += 1
            db.session.commit()
        else:
            new_stats = Stats(user_id=user.id, workouts_created=1)
            db.session.add(new_stats)
            db.session.commit()

        return redirect(url_for('workouts'))
    # GET route
    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("Please login", category="error")
        return render_template('index.html')
    # get exercises    
    exercises = Exercise.query.all()
    # get workout types
    types = WorkoutType.query.all()
    return render_template('add-workout.html', exercises=exercises, types=types)

@app.route("/select-workout", methods=['POST', 'GET'])
def select_workout():
    if request.method == 'POST':
        username = session.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Please login", category="error")
            return render_template('index.html')
        # get form data
        workout_id = request.form['workout_id']
        # print(workout_id)
        return redirect(url_for('log_workout', id=workout_id))
    # GET route
    # get users workouts
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("Please login", category="error")
        return render_template('index.html')
    user_workouts = Workout.query.filter_by(user_id=user.id).all()
    
    return render_template('select-workout.html', workouts=user_workouts)

@app.route("/log-workout/<id>", methods=['POST', 'GET'])
def log_workout(id):
    if request.method == 'POST':
        username = session.get('username')
        user = User.query.filter_by(username=username).first()

        if not user:
            flash("You must be signed in to create a workout", category="error")
            return render_template('index.html')
        
        # get form info
        exercise_ids = request.form.getlist('exercise_id')
        set_nums = request.form.getlist('set_num')
        weights = request.form.getlist('weight')
        reps = request.form.getlist('reps')

        # Group sets by exercise # copilot used for help with grouping data
        grouped_sets = defaultdict(list)
        for exercise_id, set_num, weight, rep in zip(exercise_ids, set_nums, weights, reps):
            grouped_sets[exercise_id].append({
                'set_number': int(set_num),
                'weight': int(weight),
                'reps': int(rep)
        })

        # print(grouped_sets)

        # create new training session
        new_session = TrainingSession(user_id=user.id, workout_id=id)
        db.session.add(new_session)
        db.session.commit()

        # get new session id
        new_session_id = new_session.id
        

        # create new logbook 
        for exercise_id, sets in grouped_sets.items():
            new_logbook = Logbook(session_id=new_session_id, exercise_id=exercise_id)
            db.session.add(new_logbook)
            db.session.commit()
            new_logbook_id = new_logbook.id
            # log sets
            for set in sets:
                new_set = Set(logbook_id=new_logbook_id, set_number=set['set_number'], weight=set['weight'], reps=set['reps'])
                db.session.add(new_set)
        db.session.commit()

        # get stats
        existing_stats = Stats.query.filter_by(user_id=user.id).first()

        if existing_stats:
            existing_stats.workouts_completed += 1
            db.session.commit()
        else:
            new_stats = Stats(user_id=user.id, workouts_completed=1)
            db.session.add(new_stats)
            db.session.commit()

        # check if pr was broken
        bench = Exercise.query.filter_by(name='Flat barbell bench press').first()
        deadlift = Exercise.query.filter_by(name='Deadlift').first()
        squat = Exercise.query.filter_by(name='Squat').first()
        if not bench or not deadlift or not squat:
            flash("Workout logged", category="success")
            return redirect(url_for('dashboard'))
        prs = Stats.query.filter_by(user_id=user.id).first()
        for exercise_id, sets in grouped_sets.items():
            exercise_id = int(exercise_id)
            # find heaviest set weight
            top_weight = max(set['weight'] for set in sets)
            # check if any exercise pr has been broken
            if exercise_id == bench.id and top_weight > prs.bench_pr: 
                prs.bench_pr = top_weight
                flash("New bench pr set, well done!", category="success")
            if exercise_id == deadlift.id and top_weight > prs.deadlift_pr:
                prs.deadlift_pr = top_weight
                flash("New deadlift pr set, well done!", category="success")
            if exercise_id == squat.id and top_weight > prs.squat_pr:
                prs.squat_pr = top_weight
                flash("New squat pr set, well done!", category="success")
        db.session.commit()

        flash("Workout logged", category="success")
        return redirect(url_for('dashboard'))

    # GET route
    # get users workouts
    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("Please login", category="error")
        return render_template('index.html')
    
    workout = Workout.query.filter_by(id=id).first()

    exercises = db.session.query(Exercise).join(WorkoutExercise).filter(WorkoutExercise.workout_id == id).order_by(WorkoutExercise.order).all()

    # show previous workout stats during workout
    last_session = TrainingSession.query.filter_by(user_id=user.id, workout_id=id).order_by(desc(TrainingSession.date)).first()
    if last_session:
        last_log = last_session.logbooks
        print(last_log[0].sets)
        return render_template('log-workout.html', workout=workout, exercises=exercises, last_log=last_log)
    
    # print(exercises)
    return render_template('log-workout.html', workout=workout, exercises=exercises, last_log=None )

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        # get form data
        squat = request.form['squat']
        bench = request.form['bench']
        deadlift = request.form['deadlift']

        # check if users alrewady exists in stats model
        username = session.get('username')
        user = User.query.filter_by(username=username).first()
        existing_stats = Stats.query.filter_by(user_id=user.id).first()
        if existing_stats:
            existing_stats.squat_pr = squat
            existing_stats.bench_pr = bench
            existing_stats.deadlift_pr = deadlift
        else:
            new_stats = Stats(user_id=user.id, squat_pr=squat, bench_pr=bench, deadlift_pr=deadlift)
            db.session.add(new_stats)
        db.session.commit()
        return redirect(url_for('dashboard'))
        
    # get route
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("You must be signed in to view dashboard", category="error")
        return render_template('index.html')
    stats = Stats.query.filter_by(user_id=user.id).first()
    last_session = TrainingSession.query.filter_by(user_id=user.id).order_by(desc(TrainingSession.date)).first()
    if last_session:
        last_workout = Workout.query.filter_by(id=last_session.workout_id).first()
        last_log = last_session.logbooks
        if stats:
            return render_template('dashboard.html', last_workout=last_workout, last_log=last_log, stats=stats)
    if stats:
        return render_template('dashboard.html', last_workout=None, last_log=None, stats=stats)
    return render_template('dashboard.html', last_workout=None, last_log=None, stats=None)

@app.route('/delete-workout', methods=['POST'])
def delete_workout():
    id = request.form['workout-id']
    workout = Workout.query.filter_by(id=id).first()
    print(id, workout)
    if workout:
        db.session.delete(workout)
        db.session.commit()
    return redirect(url_for('workouts'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)