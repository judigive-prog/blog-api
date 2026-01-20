from rest_framework import serializers
from .models import Post, Category, Tags, User
from rest_framework.relations import StringRelatedField

class PostSerializer(serializers.ModelSerializer):
    tags = StringRelatedField(many=True)
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Post
        fields = '__all__'

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