import hashlib
import hmac
import base64
import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404, render

from .models import TeleMATSession


def index(request):
    template_name = "index.html"
    context = {"sessions": TeleMATSession.objects.all()}
    return render(request, template_name, context)


def session(request, session_id):
    session = get_object_or_404(TeleMATSession, pk=session_id)
    meeting_id = session.zoom_created_response["id"]
    template_name = "session.html"
    signature_data = {
        "apiKey": settings.ZOOM_SDK_KEY,
        "apiSecret": settings.ZOOM_SDK_SECRET,
        "meetingNumber": meeting_id,
        "role": 0,
    }
    context = {
        "zoom_sdk_key": settings.ZOOM_SDK_KEY,
        "zoom_meeting_signature": generateSignature(signature_data),
        "zoom_meeting_id": meeting_id,
    }
    return render(request, template_name, context)


def generateSignature(data):
    ts = int(round(datetime.datetime.utcnow().timestamp() * 1000))
    msg = data["apiKey"] + str(data["meetingNumber"]) + str(ts) + str(data["role"])
    message = base64.b64encode(bytes(msg, "utf-8"))
    secret = bytes(data["apiSecret"], "utf-8")
    meeting_hmac = hmac.new(secret, message, hashlib.sha256)
    meeting_encoded = base64.b64encode(meeting_hmac.digest())
    meeting_hash = meeting_encoded.decode("utf-8")
    tmpString = "%s.%s.%s.%s.%s" % (
        data["apiKey"],
        str(data["meetingNumber"]),
        str(ts),
        str(data["role"]),
        meeting_hash,
    )
    signature = base64.b64encode(bytes(tmpString, "utf-8"))
    signature = signature.decode("utf-8")
    return signature.rstrip("=")
