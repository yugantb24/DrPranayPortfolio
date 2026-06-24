# Physiotherapy Clinic Management & Appointment Booking System

This Django project provides a modern, responsive website for a physiotherapy clinic with patient registration, online booking, testimonials, public pages, and a custom admin workflow.

## Features
- Public homepage, about, services, booking, testimonials, contact, gallery, and FAQ pages
- Patient registration/login and dashboard
- Appointment booking with slot protection and status tracking
- Testimonials moderation flow
- Admin-ready models for clinic profile, services, gallery, FAQs, appointments, and contact messages
- SQLite database with seed data for local development

## Setup
1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:
   ```bash
   python3 -m pip install Django pillow
   ```
3. Run migrations:
   ```bash
   python3 manage.py migrate
   ```
4. Seed starter content:
   ```bash
   python3 manage.py seed_clinic
   ```
5. Start the development server:
   ```bash
   python3 manage.py runserver
   ```
6. Open http://127.0.0.1:8000/

## Admin access
Create a superuser:
```bash
python3 manage.py createsuperuser
```
Then sign in at http://127.0.0.1:8000/admin/.

## Notes
- The app uses Django's built-in auth system.
- Email delivery is currently routed to the console for development.
- The site is ready for PostgreSQL by switching the database configuration in settings.py.
