import os
import sys
from pathlib import Path
from datetime import date, time, timedelta

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imhotep_smart_clinic.settings')
django.setup()

from accounts.models import User
from doctor.models import DoctorProfile, Patients, Appointments, AppointmentTimes

def main():
    doctor_user = User.objects.get(username='imani')
    doctor_profile = DoctorProfile.get_or_create_for_user(doctor_user)
    clinic = doctor_profile.clinic

    print(f"Setting up appointment schedules and appointments for Doctor: {doctor_profile} at {clinic}")

    # 1. Setup weekly appointment time slots if not already configured
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for day in days_of_week:
        slot, created = AppointmentTimes.objects.get_or_create(
            doctor=doctor_profile,
            day_of_the_week=day,
            defaults={
                'start_time': time(9, 0),
                'end_time': time(17, 0),
                'separation_time': timedelta(minutes=30),
                'activated_status': True
            }
        )
        if created:
            print(f"Created weekly appointment slot: {day} 09:00 - 17:00 (30 mins)")

    # 2. Appointments data for each patient
    # Note: today is 2026-11-11
    appointments_data = [
        # Amina Hassan
        {
            "patient_name": "Amina Hassan",
            "appointments": [
                {"date": date(2026, 8, 10), "time": time(10, 30), "status": "completed"},
                {"date": date(2026, 9, 18), "time": time(14, 0), "status": "completed"},
                {"date": date(2026, 11, 11), "time": time(11, 0), "status": "completed"},  # Today, completed
                {"date": date(2026, 11, 18), "time": time(10, 0), "status": "scheduled"},  # Upcoming
                {"date": date(2026, 12, 9), "time": time(11, 30), "status": "scheduled"},   # Upcoming
            ]
        },
        # David Ochieng
        {
            "patient_name": "David Ochieng",
            "appointments": [
                {"date": date(2026, 7, 15), "time": time(11, 0), "status": "completed"},
                {"date": date(2026, 9, 5), "time": time(15, 30), "status": "completed"},
                {"date": date(2026, 10, 28), "time": time(10, 0), "status": "completed"},
                {"date": date(2026, 11, 13), "time": time(14, 30), "status": "scheduled"},  # Upcoming
                {"date": date(2026, 12, 4), "time": time(9, 30), "status": "scheduled"},    # Upcoming
            ]
        },
        # Sarah Wanjiku
        {
            "patient_name": "Sarah Wanjiku",
            "appointments": [
                {"date": date(2026, 6, 20), "time": time(16, 0), "status": "completed"},
                {"date": date(2026, 8, 14), "time": time(11, 30), "status": "completed"},
                {"date": date(2026, 10, 12), "time": time(14, 0), "status": "completed"},
                {"date": date(2026, 11, 11), "time": time(15, 0), "status": "scheduled"},  # Today, scheduled
                {"date": date(2026, 11, 25), "time": time(11, 0), "status": "scheduled"},  # Upcoming
            ]
        },
        # Peter Kiprop
        {
            "patient_name": "Peter Kiprop",
            "appointments": [
                {"date": date(2026, 7, 2), "time": time(9, 30), "status": "completed"},
                {"date": date(2026, 8, 25), "time": time(12, 30), "status": "completed"},
                {"date": date(2026, 10, 30), "time": time(16, 0), "status": "completed"},
                {"date": date(2026, 11, 16), "time": time(10, 30), "status": "scheduled"},  # Upcoming
                {"date": date(2026, 12, 8), "time": time(14, 0), "status": "scheduled"},   # Upcoming
            ]
        },
        # Fatuma Mohamed
        {
            "patient_name": "Fatuma Mohamed",
            "appointments": [
                {"date": date(2026, 8, 1), "time": time(10, 0), "status": "completed"},
                {"date": date(2026, 9, 10), "time": time(11, 0), "status": "completed"},
                {"date": date(2026, 11, 5), "time": time(15, 0), "status": "completed"},
                {"date": date(2026, 11, 19), "time": time(11, 30), "status": "scheduled"},  # Upcoming
                {"date": date(2026, 12, 15), "time": time(10, 0), "status": "scheduled"},  # Upcoming
            ]
        },
        # Jared Ndolo
        {
            "patient_name": "Jared Ndolo",
            "appointments": [
                {"date": date(2026, 11, 10), "time": time(10, 0), "status": "completed"},
                {"date": date(2026, 11, 20), "time": time(15, 0), "status": "scheduled"},
            ]
        }
    ]

    total_created = 0
    past_count = 0
    upcoming_count = 0

    for item in appointments_data:
        patient = Patients.objects.filter(name=item["patient_name"], doctor=doctor_profile).first()
        if not patient:
            print(f"Warning: Patient {item['patient_name']} not found for doctor {doctor_profile}")
            continue

        print(f"\nProcessing appointments for {patient.name}:")
        for apt in item["appointments"]:
            appointment, created = Appointments.objects.get_or_create(
                doctor=doctor_profile,
                date=apt["date"],
                start_time=apt["time"],
                defaults={
                    "patient": patient,
                    "clinic": clinic,
                    "status": apt["status"]
                }
            )
            if not created:
                appointment.patient = patient
                appointment.clinic = clinic
                appointment.status = apt["status"]
                appointment.save()

            if apt["status"] == "completed":
                past_count += 1
            else:
                upcoming_count += 1
            total_created += 1

            status_label = "[PAST/COMPLETED]" if apt["status"] == "completed" else "[UPCOMING/SCHEDULED]"
            print(f"  {status_label} {apt['date'].strftime('%Y-%m-%d')} at {apt['time'].strftime('%H:%M')}")

    print(f"\nSummary:")
    print(f"  Total appointments processed: {total_created}")
    print(f"  Past / Completed: {past_count}")
    print(f"  Upcoming / Scheduled: {upcoming_count}")

if __name__ == '__main__':
    main()

