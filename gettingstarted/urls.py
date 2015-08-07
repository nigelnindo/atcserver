from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

import hello.views
from rest_framework.authtoken import views

from api.views import(ViewUserProfiles,ViewQuestions,
        ViewQuestionAndComments, ViewComments, ActionUserSignUp,
        ViewImages, UploadImage, UploadTestImage)

from tellkanju.views import ViewAllReports, UploadReport, TryToken


from atcfinals.views import (ViewInnovators,ViewInnovator,
    FindInnovatorsByKeyWord,ViewIdeas,GetComments,GetLikes,
    ViewInnovatorExperiences,PostIdea,ActionCreateInnovator,
    ActionAddExperience,ActionComment,ActionLike,ActionUserSignUp,
    ViewIdea,GetMyProfile)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'userprofiles/$',ViewUserProfiles.as_view()),
    #url(r'questions/$',ViewQuestions.as_view()),
    #url(r'questions/(?P<id>[0-9]+)/details$',ViewQuestionAndComments.as_view()),
    #url(r'comments/$',ViewComments.as_view()),
    #url(r'pictures/$',ViewImages.as_view()),
    #url(r'pictures/upload/$',UploadImage.as_view()),
    #url(r'pictures/test/$',UploadTestImage.as_view()),
    #url(r'reports/$',ViewAllReports.as_view()),
    #url(r'reports/upload/$',UploadReport.as_view()),
    
    #finals API starts here
    url(r'signup/$',ActionUserSignUp.as_view()),
    url(r'trytoken/$',TryToken.as_view()),
    url(r'innovators/$',ViewInnovators.as_view()),
    url(r'innovators/create/$',ActionCreateInnovator.as_view()),
    url(r'innovators/myprofile/$',GetMyProfile.as_view()),
    url(r'innovators/(?P<id>[0-9]+)/$',ViewInnovator.as_view()),
    url(ur'innovators/(?P<keyword>.*)/keyword/$',FindInnovatorsByKeyWord.as_view()),
    url(r'experiences/(?P<id>[0-9]+)/$',ViewInnovatorExperiences.as_view()),
    url(r'experiences/add/$',ActionAddExperience.as_view()),
    url(r'ideas/$',ViewIdeas.as_view()),
    url(r'ideas/(?P<id>[0-9]+)/$',ViewIdea.as_view()),
    url(r'ideas/post/$',PostIdea.as_view()),
    url(r'comments/(?P<id>[0-9]+)/$',GetComments.as_view()),
    url(r'comments/(?P<id>[0-9]+)/comment/$',ActionComment.as_view()),
    url(r'likes/(?P<id>[0-9]+)/$',GetLikes.as_view()),
    url(r'likes/(?P<id>[0-9]+)/like/$',GetLikes.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token)
)



if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)