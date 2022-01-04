from .__init__ import create_app
from datetime import datetime, timedelta
from flask_twilio import Twilio
from .models import Reminder
from . import db

def check_time():
    with create_app().app_context():
        print("------------- the time is...", datetime.now(), flush=True)

        now = datetime(2021, 1, 1, hour=21, minute=2, second=0)
        this_time = now.time()
        three_mins_ago = (now - timedelta(minutes=3)).time()

        reminders = Reminder.query.filter(Reminder.time <= this_time)
        reminders = reminders.filter(Reminder.time >= three_mins_ago)
        print("got reminders happening now:", flush=True)
        for rem in reminders:
            print(rem, flush=True)
    
        