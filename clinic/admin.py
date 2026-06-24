from django.contrib import admin

from .models import Appointment, ClinicProfile, ContactMessage, FAQ, GalleryImage, Service, Testimonial


@admin.register(ClinicProfile)
class ClinicProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "consultation_fee")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "featured")
    list_filter = ("featured",)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "rating", "approved", "created_at")
    list_filter = ("approved",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "patient_phone", "booking_date", "booking_time", "status")
    list_filter = ("status", "booking_date")
    search_fields = ("patient_name", "patient_phone", "notes")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order")
