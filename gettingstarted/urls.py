from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

import hello.views

from api.views import(ViewUserProfiles,ViewQuestions,
        ViewQuestionAndComments, ViewComments, ActionUserSignUp,
        ViewImages, UploadImage, UploadTestImage)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'userprofiles/$',ViewUserProfiles.as_view()),
    url(r'questions/$',ViewQuestions.as_view()),
    url(r'questions/(?P<id>[0-9]+)/details$',ViewQuestionAndComments.as_view()),
    url(r'comments/$',ViewComments.as_view()),
    url(r'pictures/$',ViewImages.as_view()),
    url(r'pictures/upload/$',UploadImage.as_view()),
    url(r'pictures/test/$',UploadTestImage.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)