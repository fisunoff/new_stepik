from django.contrib import admin

from certificate.models import Demand, GeneratedDocument

# Register your models here.
admin.site.register(Demand)
admin.site.register(GeneratedDocument)
