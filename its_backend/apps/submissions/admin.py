from django.contrib import admin

from .models import ITSFeedback, Submissiondata

# Register your models here.
admin.site.register(Submissiondata)
admin.site.register(ITSFeedback)
