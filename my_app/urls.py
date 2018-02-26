from django.urls import path
from . import views
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

app_name = 'my_app'
urlpatterns = [
    path('', views.MainPage.as_view(), name='main-page'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('add-link', views.AddLink.as_view(), name='add-link'),
    path('show-link/<slug:slug>', views.ShowLink.as_view(), name='show-link'),
    path('<slug:slug>', views.GetLink.as_view(), name='get-link'),
    path('give-content/<slug:slug>', views.GiveLink.as_view(),
         name='give-content'),
    path('api/info-list', views.InfoList.as_view(), name='get-info'),
    # path('api/add', views.AddContent.as_view(), name='add-content'),



]
# # serve static file
# urlpatterns += [
#         re_path(r'^uploads/(?P<path>.*)$', serve, {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#     ]

# url(r'^show_link/(?P<slug>[\w-]+)/$', views.ShowLink.as_view(),
#     name='show-link')
