from rest_framework import serializers
from .models import Post, Category, Tags
from rest_framework.relations import StringRelatedField

class PostSerializer(serializers.ModelSerializer):
    tags = StringRelatedField(many=True)
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