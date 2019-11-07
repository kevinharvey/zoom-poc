from django.conf import settings
from django.shortcuts import render


def index(request):
    template_name = "index.html"
    context = {
        "ZOOM_SDK_KEY": settings.ZOOM_SDK_KEY,
        "ZOOM_SDK_SECRET": settings.ZOOM_SDK_SECRET,
    }
    return render(request, template_name, context)


signature_data = {
    "apiKey": settings.ZOOM_SDK_KEY,
    "apiSecret": settings.ZOOM_SDK_SECRET,
    "meetingNumber": "652905629",
    "role": 0,
}

