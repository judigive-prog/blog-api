from django.shortcuts import render
from rest_framework import viewsets
from .models import Post, Category, Tags, User, Comment
from .serializers import PostSerializer, CategorySerializer, TagsSerializer, UserSerializer, RegistrationSerializer, CommentSerializer
from rest_framework import permissions
from blogApi.blog import permissions
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.generics import CreateAPIView
from .filters import PostFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.db import models
from rest_framework import mixins
# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [permissions.IsAuthorOrReadOnly]
    filterset_class = PostFilter

    ordering_fields = ['created_at', 'updated_at', 'likes_count']
    ordering = ['created_at']

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('likes')
        if self.request.user.is_authenticated:
            return queryset.filter(models.Q(draft=False) | models.Q(author=self.request.user))
        return queryset.filter(draft=False)

    def perform_update(self, serializer):
        snippet = self.get_object()
        if snippet.draft:
            return super().perform_update(serializer)
        raise ValidationError({'error': 'Post is already published'})

    @action(detail=True, methods=['post', 'get'], permission_classes=[permissions.IsOwner])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.draft = False
        post.save()
        return Response({'status': 'post published'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'get'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'status': 'post unliked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({'status': 'post liked'}, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        serializer_class=CommentSerializer,
        url_path='add-comment'
    )
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            post=post,
            author=request.user
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

class CommentViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(
        detail=True,
        methods=["post", "get"],
        permission_classes=[IsAuthenticated],
    )
    def like(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.likes.filter(id=self.request.user.id).exists():
            comment.likes.remove(self.request.user)
            return Response(status=204)
        else:
            comment.likes.add(self.request.user)
            return Response(status=204)

    @action(
        detail=True,
        methods=["post", "get"],
        permission_classes=[IsAuthenticated],
    )
    def add_comment(self, request, pk=None):
        parent_comment = self.get_object()
        if request.method == "GET":
            serializer = self.get_serializer()
            return Response(serializer.data)

        # Si es POST, procesamos los datos
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(
                author=request.user,
                parent=parent_comment,
                post=parent_comment.post,
            )
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)