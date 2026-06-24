from datetime import date, time

from django.db import IntegrityError
from django.test import TestCase

from .models import Appointment, ClinicProfile


class ClinicModelsTests(TestCase):
    def test_clinic_profile_defaults(self):
        profile = ClinicProfile.objects.create(name="Dr. Pranay")
        self.assertEqual(profile.name, "Dr. Pranay")
        self.assertEqual(profile.consultation_fee, 1000)

    def test_prevents_double_booking_for_visitors(self):
        Appointment.objects.create(
            patient_name="Asha",
            patient_phone="9876543210",
            booking_date=date(2026, 7, 1),
            booking_time=time(10, 0),
        )

        with self.assertRaises(IntegrityError):
            Appointment.objects.create(
                patient_name="Asha",
                patient_phone="9876543210",
                booking_date=date(2026, 7, 1),
                booking_time=time(10, 0),
            )
