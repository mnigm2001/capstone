from celery import shared_task
from django.utils import timezone
from .models import PillIntake, PillReminder
import datetime

@shared_task
def check_and_send_reminders():
    now = timezone.now()
    for intake in PillIntake.objects.filter(reminders__active=True).distinct():
        last_reminder_sent = PillReminder.objects.filter(pill_intake=intake, active=True).latest('created_at').created_at
        next_reminder_due = last_reminder_sent + datetime.timedelta(hours=intake.frequency_hours)
        if now >= next_reminder_due:
            # Logic to send reminder
            send_reminder(intake)
            # Update or create a reminder instance to track this action
            PillReminder.objects.create(pill_intake=intake, reminder_time=intake.reminder_time, active=True)

def send_reminder(intake):
    # Implement the logic to send the actual reminder here
    print(f"Reminder sent for {intake.pill.name} to {intake.user.email}")
