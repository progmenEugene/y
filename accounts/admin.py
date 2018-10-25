from django.contrib import admin

from .models import TeacherProfile, VideoLink
from django.utils.translation import ugettext_lazy as _
from .models import CustomUser






admin.site.register(CustomUser)
admin.site.register(TeacherProfile)