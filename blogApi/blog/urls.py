from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blogApi.blog import views

router = DefaultRouter()
router.register(r'post', views.PostViewSet, basename='post')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'tags', views.TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
]