from django.contrib import admin

from .models import (UserProfile,Question,
		QuestionComment, UserProfileImage, ImageTests)

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(QuestionComment)
admin.site.register(UserProfileImage)
admin.site.register(ImageTests)