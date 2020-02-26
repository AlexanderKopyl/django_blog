from django.urls import path, include
from . import views
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('posts', views.PostView)

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    # path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('api/', include(router.urls))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

