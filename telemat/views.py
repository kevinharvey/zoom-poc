import hashlib
import hmac
import base64
import datetime

from django.conf import settings
from django.shortcuts import render


def index(request):
    template_name = "index.html"
    signature_data = {
        "apiKey": settings.ZOOM_SDK_KEY,
        "apiSecret": settings.ZOOM_SDK_SECRET,
        "meetingNumber": "652905629",
        "role": 0,
    }
    context = {
        "ZOOM_SDK_KEY": settings.ZOOM_SDK_KEY,
        "ZOOM_MEETING_SIGNATURE": generateSignature(signature_data),
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
