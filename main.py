from flask import Blueprint, render_template, redirect, request, flash, session
from flask_login import login_required, current_user
from .models import Reminder
from . import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    print("dhsjfhdsjfasd", flush=True)
    
    if request.method == 'POST':
        print("posted", request, flush=True)

        # button from form to add new reminder
        if 'add' in request.form:
            name = request.form.get('name')
            dosage = request.form.get('dosage')
            notes = request.form.get('notes')
            hour = int(request.form.get('hour'))
            minute = int(request.form.get('minute'))
            am_pm = request.form.get('am_pm')

            # make pretty string representing time
            timestring = f"{hour}:{minute:02} {am_pm}"

            # get datetime.time object representing hour and minute
            if am_pm == 'AM' and hour == 12:
                hour = 0
            elif am_pm == 'PM' and hour != 12:
                hour = hour + 12
            dtime = datetime(2021, 1, 1, hour=hour, minute=minute).time()

            reminder = Reminder(name=name, dosage=dosage, notes=notes, time=dtime, timestring=timestring, user=current_user)
            db.session.add(reminder)
            db.session.commit()

            flash('Added new reminder.', category='info')
            return render_template('profile.html')
        
        # button from delete button on a reminder
        else:
            rem_id = request.form.to_dict()['idToDelete']
            # request.method should be in form "delete <reminder id>"
            
            rem = Reminder.query.get(rem_id)
            db.session.delete(rem)
            db.session.commit()

            flash("Reminder deleted.", category="info")
            return render_template('profile.html')

    else:
        return render_template('profile.html')

@main.route('/test', methods=['GET', 'POST'])
def test():
    print("------------- the time is...", datetime.now(), flush=True)

    now = datetime.now()
    this_time = datetime(2021, 1, 1, hour=21, minute=2, second=0).time()

    # filter by hour first
    reminders = Reminder.query.filter_by(name="EEEEE")
    print("got reminders happening now:", reminders.first(), flush=True)