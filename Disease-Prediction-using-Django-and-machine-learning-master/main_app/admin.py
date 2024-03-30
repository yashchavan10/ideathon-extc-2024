from django.contrib import admin
from .models import disease_info, patient , doctor , diseaseinfo , consultation,rating_review

# Register your models here.

admin.site.register(patient)
admin.site.register(doctor)
admin.site.register(diseaseinfo)
admin.site.register(disease_info)
admin.site.register(consultation)
admin.site.register(rating_review)