from django.contrib import admin

from .models import TeleMATSession


@admin.register(TeleMATSession)
class TeleMATSessionAdmin(admin.ModelAdmin):
    pass
