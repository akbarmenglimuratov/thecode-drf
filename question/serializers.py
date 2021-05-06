from rest_framework import serializers
from question.models import Question, Answer, Comment
from django.contrib.auth.models import User
from tag.models import Tag

class AuthorSerializer(serializers.Serializer):
	username = serializers.CharField()
	first_name = serializers.CharField()
	last_name = serializers.CharField()

class CommentSerializer(serializers.ModelSerializer):
	author = AuthorSerializer()
	_votes = serializers.SerializerMethodField()
	
	class Meta:
		model = Comment
		exclude = ['upvote', 'downvote', 'question']

	def get__votes(self,obj):
		up = obj.upvote.count()
		down = obj.downvote.count()
		return up - down
	

class CommentCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comment
		fields = '__all__'
		read_only_fields = ['author', 'question']

class AnswerSerializer(serializers.ModelSerializer):
	author = AuthorSerializer()
	_votes = serializers.SerializerMethodField()
	
	class Meta:
		model = Answer
		exclude = ['upvote', 'downvote', 'question']

	def get__votes(self,obj):
		up = obj.upvote.count()
		down = obj.downvote.count()
		return up - down
	
class AnswerCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Answer
		fields = '__all__'
		read_only_fields = ['author', 'question']

class TagSerializer(serializers.ModelSerializer):

	class Meta:
		model = Tag
		fields = ('name', 'slug',)

class QuestionListSerializer(serializers.ModelSerializer):
	author = AuthorSerializer()
	_votes = serializers.SerializerMethodField()
	tag = TagSerializer(many=True)
	class Meta:
		model = Question
		fields = ['id', 'author', 'created','title','slug', '_votes', 'tag']

	def get__votes(self,obj):
		up = obj.upvote.count()
		down = obj.downvote.count()
		return up - down
	

class QuestionDetailSerializer(serializers.ModelSerializer):
	author = AuthorSerializer()
	answers = AnswerSerializer(many = True, read_only = True, source = 'answered_question')
	comments = CommentSerializer(many = True, read_only = True, source = 'commented_question')
	_votes = serializers.SerializerMethodField()
	tag = TagSerializer(many=True)
	class Meta:
		model = Question
		exclude = ['follower', 'favorite', 'upvote', 'downvote']

	def get__votes(self,obj):
		up = obj.upvote.count()
		down = obj.downvote.count()
		return up - down

class QuestionCreateSerializer(serializers.ModelSerializer):
	tag = serializers.SlugRelatedField(queryset = Tag.objects.all(),many=True,slug_field='name')
	class Meta:
		model = Question
		fields = ['title', 'description', 'tag']


class AnswerToQuestionSerializer(serializers.ModelSerializer):
	description = serializers.CharField()

	class Meta:
		model = Answer
		fields = ['description']

class VoteSerializer(serializers.Serializer):
	pk = serializers.IntegerField()
	vote = serializers.IntegerField()

class EmptySerializer(serializers.Serializer):
	# more = serializers.CharField()
	pass
