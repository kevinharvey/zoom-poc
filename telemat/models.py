from datetime import datetime, timedelta

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings

import jwt
import requests


class TeleMATSession(models.Model):
    zoom_created_response = JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.zoom_created_response is None:
            self.zoom_created_response = self._create_meeting()
        super().save(*args, **kwargs)

    def _create_meeting(self):
        payload = {
            "iss": settings.ZOOM_SDK_KEY,
            "exp": datetime.now() + timedelta(hours=1),
        }
        token = jwt.encode(payload, settings.ZOOM_SDK_SECRET)

        h = {"Authorization": f"Bearer {token.decode()}"}
        url = f"https://api.zoom.us/v2/users/{settings.ZOOM_USER_ID}/meetings/"
        resp = requests.post(url, json={}, headers=h)

        return resp.json()
