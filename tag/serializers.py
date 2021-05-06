from rest_framework import serializers
from .models import Tag
from question.models import Question
from question.serializers import TagSerializer

class AuthorSerializer(serializers.Serializer):
	username = serializers.CharField()
	first_name = serializers.CharField()
	last_name = serializers.CharField()

class TagListSerializer(serializers.ModelSerializer):
	_tagged = serializers.SerializerMethodField()
	class Meta:
		model = Tag
		fields = '__all__'

	def get__tagged(self, tag):
		return tag.tagged.count()

class TagSerializer(serializers.ModelSerializer):

	class Meta:
		model = Tag
		fields = ('name', 'slug',)

class QuestionSerializer(serializers.ModelSerializer):
	author = AuthorSerializer()
	_votes = serializers.SerializerMethodField()
	tag = TagSerializer(many=True)
	class Meta:
		model = Question
		fields = ('id', 'author', 'created','title','slug', '_votes', 'tag')

	def get__votes(self,obj):
		up = obj.upvote.count()
		down = obj.downvote.count()
		return up - down

class TagDetailSerializer(serializers.ModelSerializer):
	tagged = QuestionSerializer(many=True)
	class Meta:
		model = Tag
		lookup_field = 'slug'
		fields = '__all__'

class EmptySerializer(serializers.Serializer):
	pass
