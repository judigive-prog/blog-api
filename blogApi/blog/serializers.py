from rest_framework import serializers
from .models import Post, Category, Tags, User, Comment
from rest_framework.relations import StringRelatedField

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    replies = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'like_count', 'replies']
        
class PostSerializer(serializers.ModelSerializer):
    tags = StringRelatedField(many=True)
    author = serializers.ReadOnlyField(source='author.username')
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'category', 'created_at', 'updated_at', 'author', 'draft', 'tags', 'like_count', 'comments']

class CategorySerializer(serializers.ModelSerializer):
    posts = StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'

class TagsSerializer(serializers.ModelSerializer):
    posts = StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Tags
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'id']
        model = User

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

