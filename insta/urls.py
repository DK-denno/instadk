from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
    url(r'^$',views.index,name="index"),
    url(r'auth/',include('registration.backends.simple.urls')),
    url(r'^sign/$',views.signup, name='signup'),
    url(r'^profile/$',views.profile, name='profile'),
    url(r'^prof/(\d+)',views.profiles,name='prof'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^follow/(?P<operation>.+)/(?P<id>\d+)',views.follow,name='follow'),
    url(r'^comment/(\d+)',views.comment,name='comment'),
    url(r'^like/(\d+)',views.likes,name='likes'),
    url(r'^search',views.search_results,name='search_results'),
    url(r'^one/(\d+)',views.one,name="one")
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)