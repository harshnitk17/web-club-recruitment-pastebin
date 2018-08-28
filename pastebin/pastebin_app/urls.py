from . import views
from django.conf.urls import url
from django.urls import path

app_name = 'pastebin_app'
urlpatterns = [

url(r'^home/$', views.Home, name="home"),
url(r'^post/(?P<random_url>[-\w]+)/$', views.post, name="post"),
url(r'^edit/(?P<random_url>[-\w]+)/$', views.edit, name="edit"),
url(r'^logout/(?P<random_id>[-\w]+)/$', views.logout, name="logout"),
url(r'^deleted/(?P<random_id>[-\w]+)/$', views.deleted, name="deleted"),
url(r'^userpage/(?P<random_id>[-\w]+)/$', views.userpage, name="userpage"),
url(r'^share/(?P<random_url>[-\w]+)/$', views.share, name="share"),
url(r'^share_edited/(?P<random_url>[-\w]+)/$', views.share_edited, name="share_edited"),
url(r'^share/(?P<random_url>[-\w]+)/s_edit/$', views.s_edit, name="s_edit"),
url(r'^delete/(?P<random_url>[-\w]+)/$', views.delete, name="delete"),
path('confirmation/', views.confirmation, name='confirmation'),
path('signup/', views.signup, name='signup'),
url(r'^userpage/(?P<random_id>[-\w]+)/mypost/$', views.mypost, name="mypost"),
]