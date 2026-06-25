from datetime import date, time

from django.conf import settings
from django.db import models
from django.utils import timezone


class ClinicProfile(models.Model):
    name = models.CharField(max_length=120)
    title = models.CharField(max_length=120, default="Senior Physiotherapist")
    bio = models.TextField(default="Compassionate care for pain relief and recovery.")
    qualifications = models.TextField(default="BPT, MPT")
    certifications = models.TextField(default="Certified Manual Therapist")
    specializations = models.TextField(default="Sports Injury, Posture Correction")
    experience_years = models.PositiveIntegerField(default=10)
    phone = models.CharField(max_length=20, default="+91 98765 43210")
    email = models.EmailField(default="clinic@example.com")
    address = models.TextField(default="123 Wellness Avenue")
    google_maps_link = models.URLField(blank=True)
    consultation_fee = models.PositiveIntegerField(default=1000)
    clinic_timings = models.TextField(default="Mon-Sat: 9am to 7pm")
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    facebook_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="fas fa-heart")
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    title = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to="gallery/")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title or "Gallery Image"


class Testimonial(models.Model):
    patient_name = models.CharField(max_length=120)
    patient_phone = models.CharField(max_length=20, blank=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.patient_name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]
    patient_name = models.CharField(max_length=120, blank=True)
    patient_phone = models.CharField(max_length=20, blank=True)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="Pending")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["booking_date", "booking_time"], name="unique_booking_slot")
        ]

    def __str__(self):
        return f"{self.patient_name} - {self.booking_date} {self.booking_time}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.question
