from datetime import datetime, timedelta
from .models import Reminder
from . import db
import os
from twilio.rest import Client
from dotenv import load_dotenv

#TODO: change this once done testing
# minute tolerance for checking older reminders
TOLERANCE = 60
DEBUG = True

# load secret environment variables
load_dotenv()

client = Client(os.environ['TWILIO_SID'], os.environ['TWILIO_AUTH'])

def send_reminders(scheduler):
    with scheduler.app.app_context():
        #print("------------- the time is...", datetime.now(), flush=True)

        now = datetime.now()

        this_time = now.time()
        earlier_time = (now - timedelta(minutes=TOLERANCE)).time()
        #print(this_time, earlier_time)

        reminders = Reminder.query.filter(Reminder.time <= this_time)
        reminders = reminders.filter(Reminder.time >= earlier_time)

        if DEBUG: print("reminders happening now:", flush=True)

        for rem in reminders:
            if DEBUG: print(rem, rem.time, flush=True)

            if rem.lastnotif < now.date():
                # a reminder hasn't been sent yet today
                if DEBUG: print('havent reminded yet today; texting', rem, flush=True)
                
                # get user's phone number
                phone = rem.user.phone

                if phone:
                    msg = f"{rem.name} [{rem.dosage}]\n{rem.notes}"
                    client.messages.create(to=phone, from_="+15878585813", body=msg)
                elif DEBUG:
                    print(f"No phone specified for user {rem.user.id}.", flush=True)
                
                # set 'lastnotif' to today so we know not to text again today
                rem.lastnotif = now.date()

        db.session.commit()
