from django.shortcuts import render
from rest_framework import viewsets
from .models import Post, Category, Tags, User
from .serializers import PostSerializer, CategorySerializer, TagsSerializer, UserSerializer, RegistrationSerializer
from rest_framework import permissions
from blogApi.blog import permissions
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.generics import CreateAPIView
# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [permissions.IsAuthorOrReadOnly]

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = []