from django.core.management.base import BaseCommand

from clinic.models import ClinicProfile, FAQ, GalleryImage, Service, Testimonial


class Command(BaseCommand):
    help = "Seed the clinic site with starter content"

    def handle(self, *args, **options):
        profile, _ = ClinicProfile.objects.get_or_create(
            name="Dr. Pranay",
            defaults={
                "title": "Senior Physiotherapist",
                "bio": "Dr. Pranay is a compassionate physiotherapist focused on restoring movement, reducing pain, and helping patients return to daily life with confidence.",
                "qualifications": "BPT, MPT, Certified Manual Therapy Specialist",
                "certifications": "Sports Rehab, Dry Needling, Postural Alignment",
                "specializations": "Sports Injury, Post-operative Rehab, Spine Care",
                "experience_years": 12,
                "phone": "+91 98765 43210",
                "email": "care@physiocare.com",
                "address": "123 Wellness Avenue, Pune",
                "google_maps_link": "https://maps.google.com",
                "consultation_fee": 1000,
                "clinic_timings": "Mon-Sat: 9am to 7pm",
            },
        )

        services = [
            ("Manual Therapy", "Hands-on treatment to reduce pain and improve mobility.", "fas fa-hands"),
            ("Posture Correction", "Targeted exercises for spinal correction and balance.", "fas fa-spine"),
            ("Sports Rehabilitation", "Performance-focused recovery plans after injury.", "fas fa-running"),
        ]
        for name, desc, icon in services:
            Service.objects.get_or_create(name=name, defaults={"description": desc, "icon": icon, "featured": True})

        FAQ.objects.get_or_create(question="Do you accept walk-ins?", defaults={"answer": "Yes, subject to availability. Online booking is recommended.", "order": 1})
        FAQ.objects.get_or_create(question="How long is a typical session?", defaults={"answer": "Most sessions last between 45 and 60 minutes.", "order": 2})

        Testimonial.objects.get_or_create(
            patient_name="Riya S.",
            defaults={"content": "The recovery plan helped me return to running after my knee injury.", "rating": 5, "approved": True},
        )

        self.stdout.write(self.style.SUCCESS("Seed data loaded successfully."))
