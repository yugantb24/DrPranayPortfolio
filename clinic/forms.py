from django import forms

from .models import Appointment, ContactMessage, Testimonial


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["patient_name", "patient_phone", "booking_date", "booking_time", "notes"]
        widgets = {
            "booking_date": forms.DateInput(attrs={"type": "date"}),
            "booking_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get("booking_date")
        booking_time = cleaned_data.get("booking_time")
        if booking_date and booking_time and Appointment.objects.filter(booking_date=booking_date, booking_time=booking_time).exists():
            raise forms.ValidationError("This time slot has already been booked. Please choose another one.")
        return cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["patient_name", "patient_phone", "content", "rating"]
