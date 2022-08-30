from django.contrib import admin

# Register your models here.
from hotel.models import Dishes,Review
admin.site.register(Dishes)
admin.site.register(Review)