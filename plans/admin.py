from django.contrib import admin
from .models import Plan, Investment, RoiAmount


admin.site.register(Plan)
admin.site.register(Investment)
admin.site.register(RoiAmount)
