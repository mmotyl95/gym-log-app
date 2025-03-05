from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Workout
from app.forms import WorkoutForm

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).all()
    return render_template('dashboard.html', workouts=workouts)

@main.route('/add_workout', methods=['GET', 'POST'])
@login_required
def add_workout():
    form = WorkoutForm()
    if form.validate_on_submit():
        workout = Workout(
            user_id=current_user.id,
            exercise=form.exercise.data,
            sets=form.sets.data,
            reps=form.reps.data,
            weight=form.weight.data or 0
        )
        db.session.add(workout)
        db.session.commit()
        flash('Workout added successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_workout.html', form=form)