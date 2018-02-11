from django.urls import path
from . import views

app_name = 'my_app'
urlpatterns = [
    path('', views.MainPage.as_view(), name='main-page'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('add-link', views.AddLink.as_view(), name='add-link'),
    path('show-link/<slug:slug>', views.ShowLink.as_view(), name='show-link'),
]

# url(r'^show_link/(?P<slug>[\w-]+)/$', views.ShowLink.as_view(),
#     name='show-link')
