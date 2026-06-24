from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import AppointmentForm, ContactForm, TestimonialForm
from .models import Appointment, ClinicProfile, FAQ, GalleryImage, Service, Testimonial


def get_or_create_profile():
    return ClinicProfile.objects.first() or ClinicProfile.objects.create(name="Dr. Pranay")


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.filter(featured=True)[:3]
        context["testimonials"] = Testimonial.objects.filter(approved=True)[:3]
        return context


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ServicesView(TemplateView):
    template_name = "services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.all()
        return context


class BookingView(FormView):
    template_name = "booking.html"
    form_class = AppointmentForm
    success_url = reverse_lazy("booking")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["appointments"] = Appointment.objects.filter(status__in=["Pending", "Confirmed"]).order_by("booking_date", "booking_time")
        return context

    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.save()
        send_mail(
            "Appointment request received",
            f"Hello {appointment.patient_name}, your appointment for {appointment.booking_date} at {appointment.booking_time} has been received.",
            "clinic@example.com",
            [get_or_create_profile().email],
            fail_silently=True,
        )
        messages.success(self.request, "Your appointment request has been submitted.")
        return super().form_valid(form)


class TestimonialsView(TemplateView):
    template_name = "testimonials.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["testimonials"] = Testimonial.objects.filter(approved=True)
        context["form"] = TestimonialForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your feedback will be visible after approval.")
            return redirect("testimonials")
        return render(request, self.template_name, {"form": form, "testimonials": Testimonial.objects.filter(approved=True)})


class ContactView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.save()
        send_mail(
            "New contact message",
            f"You received a new message from {form.cleaned_data['name']}: {form.cleaned_data['message']}",
            "clinic@example.com",
            [get_or_create_profile().email],
            fail_silently=True,
        )
        messages.success(self.request, "Your message has been received.")
        return super().form_valid(form)


class GalleryView(TemplateView):
    template_name = "gallery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gallery_images"] = GalleryImage.objects.all()
        return context


class FAQView(TemplateView):
    template_name = "faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faqs"] = FAQ.objects.all()
        return context


