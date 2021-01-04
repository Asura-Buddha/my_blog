from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('', views.home, name='home'),
                  path('users/', views.users, name='users'),
                  path('posts/', views.post_list, name='post_list'),
                  path('post/<int:pk>/like/', views.post_like, name='post_like'),
                  path('post/<int:pk>/', views.post_page, name='post_page'),
                  path('post/new/', views.post_new, name='post_new'),
                  path('post/comment/new/', views.comment_new, name='comment_new'),
                  path('contact/', views.contact_page, name='contact_page'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
