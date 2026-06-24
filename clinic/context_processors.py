from .models import ClinicProfile


def clinic_profile(request):
    profile = ClinicProfile.objects.first()
    return {"profile": profile}
