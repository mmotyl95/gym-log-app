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
    form = WorkoutForm()
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).all()
    return render_template('dashboard.html', workouts=workouts, form=form)

@main.route('/add_workout', methods=['POST'])
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

@main.route('/edit_workout/<int:workout_id>', methods=['GET', 'POST'])
@login_required
def edit_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    
    if workout.user_id != current_user.id:
        flash("You don't have permission to edit this workout!", "danger")
        return redirect(url_for('main.dashboard'))

    form = WorkoutForm(obj=workout)

    if form.validate_on_submit():
        workout.exercise = form.exercise.data
        workout.sets = form.sets.data
        workout.reps = form.reps.data
        workout.weight = form.weight.data or 0
        db.session.commit()
        flash('Workout updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('edit_workout.html', form=form, workout=workout)

@main.route('/delete_workout/<int:workout_id>', methods=['POST'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)

    if workout.user_id != current_user.id:
        flash("You don't have permission to delete this workout!", "danger")
        return redirect(url_for('main.dashboard'))

    db.session.delete(workout)
    db.session.commit()
    flash('Workout deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

from flask import jsonify
from app.models import Workout

from flask import jsonify
from app.models import Workout

@main.route('/workout_data')
@login_required
def workout_data():
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date).all()
    
    data = {}
    for workout in workouts:
        if workout.exercise not in data:
            data[workout.exercise] = {"dates": [], "weights": [], "sets": [], "reps": []}

        data[workout.exercise]["dates"].append(workout.date.strftime("%Y-%m-%d"))
        data[workout.exercise]["weights"].append(float(workout.weight or 0))
        data[workout.exercise]["sets"].append(int(workout.sets))
        data[workout.exercise]["reps"].append(int(workout.reps))

    return jsonify(data)