from django.utils.translation  import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import User
from question.serializers import QuestionListSerializer, AnswerSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		token['name'] = user.username
		return token


class SignupSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(required = True, validators = [UniqueValidator(queryset=User.objects.all())])
	username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = User
		fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
		extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError({"password": "Password fields didn't matched."})

		return attrs

	def create(self, validated_data):
		user = User.objects.create(
			username=validated_data['username'],
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name'],
		)
		user.set_password(validated_data['password'])
		user.save()
		return user

class UserListSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'verified', 'reputation',)

class UserDetailSerializer(serializers.ModelSerializer):
	questions = QuestionListSerializer(many=True, source='question_question_related')
	answers = AnswerSerializer(many=True, source = 'question_answer_related')
	class Meta:
		model = User
		fields = (
			'id', 
			'username', 
			'first_name', 
			'last_name', 
			'verified', 
			'reputation', 
			'date_of_birth', 
			'date_joined',
			'questions',
			'answers')

class ProfileSerializer(serializers.ModelSerializer):
	questions = QuestionListSerializer(many=True, source='question_question_related', read_only=True)
	answers = AnswerSerializer(many=True, source = 'question_answer_related',read_only=True)
	class Meta:
		model = User
		exclude = ('is_staff', 'is_active', 'password', 'is_superuser','user_permissions', 'groups', 'last_login',)
		read_only_fields = ('questions', 'answers', 'date_joined', 'verified', 'reputation', 'email',)