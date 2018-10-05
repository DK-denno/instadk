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
  
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)