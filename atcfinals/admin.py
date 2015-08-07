from django.contrib import admin

from .models import Innovator, Idea, Experience, IdeaView, IdeaComment, IdeaLike

# Register your models here.
admin.site.register(Innovator)
admin.site.register(Idea)
admin.site.register(Experience)
admin.site.register(IdeaView)
admin.site.register(IdeaComment)
admin.site.register(IdeaLike)