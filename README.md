# MyFitnessJNL

#### Video Demo: <URL HERE>

### Description:

MyFitnessJNL is a web based gym diary that allows users to build and maintain workout routines.
This app makes it easy for users to:

- Create custom workouts
- Log sets, weight & reps for each exercise
- Track personal records
- Stay consistent with their goals

features:

- Workout creation & deletion
- Real-time logging of sets, weight & reps
- Workout history
- Personal record tracking
- Stat tracking

### SET UP

#### Clone or Download the Project

Download or clone the project folder to your computer.

#### Set Up Python Virtual Environment

Open a terminal in the project directory.

Run:

```
python3 -m venv flask-env
source flask-env/bin/activate
```

#### Install Dependencies

Install required packages:

```
pip install -r requirements.txt
```

#### Initialize the Database

Run the seed scripts in the seeding folder to populate the database:

```
python app.py

python seeding/exercise-type-seed.py

python seeding/exercises-seed.py

python seeding/exercise-type-join.py

python seeding/workout-type-seed.py
```

Run the Application

```
python app.py
```

Start the Flask app:
Visit http://127.0.0.1:5000 in your browser.

### File explaination

#### Seed files:

- exercise-type-seed.py: seeds db with exercise category names
- exercise-seed.py: seeds db with actual workout names
- exercise-type-join.py: joins exercise with exercise-types
- workout-type-seed.py: seeds db with workout category names

#### app.py

this contains the main bulk of the project with all routes

index() - is the home page of the application, kept pretty basic. user is asked to login in if not in session or a brief welcome message is displayed.

register() - allows the users to sign up to MyFitnessJNL through forms & updating db. A session is created upon registering to avoid users having to login after just registering. Form validation is utilised to confirm the password typed by the user is their intended password.

login() - enables the user to log into MyFitnessJNL

logout() - enables the user to log out of MyFitnessJNL

workouts() - allows the user to view, add & delete workouts. I thought about allowing the users to edit workouts but opted to keep it simple.

add_workout() - adds the users created workout to the db

select_workout() - allows the user to choose which workout they are about to perform to log its details

log_workout() -
Gets form data and saves the into to the db. Probably the most difficult feature I had to implement; having to updating multiple models from a form with dynamically rendered input fields. Required the assistance of copilot to group the form data into a more usable structure. This also contains a check for values of certain exercises to see if a personal record had been broken. Though I could have kept record of all PRs I found it more suitable to only keep track of the 'big 3' lifts (squat, bench, deadlift) as this is the most common practice amoungst the gym community.

Progression is the key focus of a gym-goer & so I ensured to display the previous sessions stats within the current log form, this way they would have a reference point on what weight/reps they should be aiming for in the current session; allowing for progressive overload.

dashboard() - Gets the data for the last workout they performed, stats on workouts completed & workouts created as well as personal records

delete_workout() - allows the users to delete workouts from their available routines for clean-up purposes if they had too many unused workouts cloggin up their selection screen

#### models.py

Defines all models for the app using SQLAlchemy.
I opted to use SQLAlchemy as I came across a few users on youtube who reccommended it & I wanted to gain experience working with an ORM.
Personally, I prefer to work with plain SQL or postgreSQL as its a bit easier for me to visualise the db as well as just for readability. I'm not against working with ORMs again in the future as I can see the benefits, just more of a personal preference for SQL.

contains:

- User: Stores user info
- ExerciseType: Categories for exercises
- Exercise: Stores individual exercise names
- ExerciseExerciseType: Join table for many-to-many relationship between exercises and exercise types.
- WorkoutType: Categories for workouts
- Workout: User-created workout routines.
- WorkoutExercise: Links exercises to workouts, with an order field for sequencing.
- TrainingSession: Represents a logged workout session.
- Logbook: Stores logged exercises for a session, links to sets performed.
- Set: Individual set performed in a workout (reps, weight, set number).
- Stats: Tracks user stats.

#### addSet.js

dynamically adds sets(weight & reps) input fields to the workout form in log-workout.html throught a click of a button - I wanted users to feel like they were in control of the workouts, with the focus on progressive overload I wanted them to feel they are able to add sets on the fly.
Also contains removeSet() which removes the last set in the parent. Opted to only remove the last set in order to not break set count but also this is the most likely one they'd remove, potentially through misclicks or double clicks. Also I wanted only one delet button per exercise so this felt like the most natural solution.

#### addWorkout.js

Dynamically adds exercise select fields to the workout creation form in addWorkout(). The form had to be dynamic as it isnt possible to know ahead of time how many exercise they wanted & the amount could change at any point during the creation.
Also contains removeExercise() to remove that specific exercise. This time rather than removing the last child it makes most sense to want to be able to remove a certain exercise.

#### add-workout.html

Page for creating a new workout. Lets users enter workout name, description, select category/type, and add multiple exercises to the workout.

#### dashboard.html

User dashboard showing personal records (PRs) for squat, bench, and deadlift. Allows users to update their PRs and view stats.

#### index.html

Home page. Greets logged-in users and displays the app logo. For guests, shows a login form.

#### layout.html

Base template for all pages. Contains the HTML structure, navigation bar, and includes Bootstrap and custom CSS. Other templates extend this.

#### log-workout.html

Page for logging a workout session. Displays workout name and exercises, shows previous logs if available, and lets users enter sets, weights, and reps for each exercise.

#### register.html

Registration page for new users. Collects email, username, password, and password confirmation.

#### select-workout.html

Lets users select one of their workouts to log. Displays workouts as cards and provides a button to add a new workout.

#### workouts.html

Lists all workouts for the user. Each workout is shown as a card with name and description, and options to delete or edit the workout.

#### styles.CSS

Contains all CSS for the app.
