from django.contrib import admin
from .models import Record
# Register your models here.


class Recordadmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email",
                    "phone", "address", "city", "state", "zipcode", "created_at")


admin.site.register(Record, Recordadmin)
