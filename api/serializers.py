
from rest_framework import serializers

from main.models import Bb, Comment


class BbSerializer(serializers.ModelSerializer):
    """Клас для виводу переліку оголошень"""
    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at')


class BbDetailSerializer(serializers.ModelSerializer):
    """Клас для виводу обраного оголошення"""

    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at', 'contacts', 'image')


class CommentSerializer(serializers.ModelSerializer):
    """Клас для виводу коментарів до оголошення"""
    model = Comment
    fields = ('bb', 'author', 'content', 'created_at')





