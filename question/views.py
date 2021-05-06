from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from rest_framework import serializers

from question.serializers import *
from question.models import Question, Answer
from tag.models import Tag

class QuestionViewset(viewsets.GenericViewSet):
	# serializer_class = QuestionSerializer

	def get_permissions(self):
		if self.action in ['destroy','partial_update', 'update']:
			return [IsAdminUser()]
		if self.action == 'create':
			return [IsAuthenticated()]
		return super(QuestionViewset, self).get_permissions()

	def get_serializer_class(self):
		if self.action == 'list':
			return QuestionListSerializer
		if self.action == 'retrieve':
			return QuestionDetailSerializer
		if self.action == 'create':
			return QuestionCreateSerializer
		if self.action == 'answer':
			return AnswerToQuestionSerializer
		if self.action == 'vote_question' or self.action == 'vote_answer':
			return VoteSerializer
		return EmptySerializer

	def get_queryset(self):
		queryset = Question.objects.all()
		return queryset

	def get_object(self):
		queryset = self.get_queryset()
		obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
		return obj

	def list(self,request):
		queryset = self.get_queryset()
		question_list = self.get_serializer(queryset,many=True)
		return Response(question_list.data)

	def retrieve(self, request, pk):
		question = self.get_object()
		serializer = self.get_serializer(question)
		return Response(serializer.data)

	def create(self, request):

		tags = request.data.get('tag', [])
		if len(tags) > 5 or len(tags) < 1:
			return Response({"success":False, "message": "Tags must be more than 1 and less than 5!"})

		for tag in tags:
			Tag.objects.get_or_create(name=tag)

		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			serializer.save(author=request.user)
		else:
			return Response(serializer.errors)
		return Response({"sucsess":True,"message": "Created!"})

	# @action(detail=True, methods=['post'], url_path = 'vote_question', permission_classes=[IsAuthenticated])
	# def answer(self,request, pk=None):


	@action(detail=True, methods=['get','post'], url_path = 'vote_question', permission_classes=[IsAuthenticated])
	def vote_question(self,request, pk=None):
		
		serializer = self.get_serializer(data=request.data,context={"pk": pk})
		if not serializer.is_valid():
			return Response({
				"success": False, 
				"message": "Bad data."}, status=400)

		question_id = request.data.get('pk', None)
		if pk != question_id:
			return Response({"success": False, "message": "Wrong questions!"}, status=400)

		question = self.get_object()
		user = request.user

		if question.author == user:
			return Response({
				"success":False, 
				"message": "You can't voted your own question!"})

		if user.reputation < 15:
			return Response({
				"success":False, 
				"message": "Your reputation score less than 15. You can't vote!"})

		if question.upvote.filter(username=user).exists() or question.downvote.filter(username=user).exists():
			return Response({
				"success": False,
				"message": "You already voted!"})

		if int(request.data['vote']) == 1:
			question.upvote.add(user)
			message = "You voted up!"
			user.reputation += 5
		elif int(request.data['vote']) == 0:
			question.downvote.add(user)
			message = "You voted down!"
			user.reputation -= 2
		else:
			return Response({
				"success":False, 
				"message":"Bad data!"}, status=400)
		question.save()
		user.save()
		return Response({"success":True, "message":message})

	@action(detail=True, methods=['post'], url_path='vote_answer', permission_classes=[IsAuthenticated])
	def vote_answer(self,request, pk=None):
		user = request.user
		data = request.data
		serializer = self.get_serializer(data = data)
			
		if not serializer.is_valid():
			return Response({
				"success": False, 
				"message": "Bad data."}, status=400)
			
		question_id = data.get('pk', None)
		if pk != question_id:
			return Response({"success": False, "message": "Wrong question!"}, status=400)

		answer = get_object_or_404(Answer, pk = data['pk'])

		if answer.question.pk != int(pk):
			return Response({
				"success":False, 
				"message": "Wrong question!"}, status=400)

		if answer.author == user:
			return Response({
				"success": False, 
				"message": "You can't vote to your own answer!"})

		if user.reputation < 15:
			return Response({
				"success":False, 
				"message": "Your reputation score less than 15. You can't vote!"})

		if answer.upvote.filter(username = user).exists() or answer.downvote.filter(username = user).exists():
			return Response({
				"success": False,
				"message": "You already voted!"})

		if int(data['vote']) == 1:
			answer.upvote.add(user)
			user.reputation += 5
			message = "You voted up!"
		elif int(data['vote']) == 0:
			answer.downvote.add(user)
			user.reputation -= 2
			message = "You voted down!"
		else:
			return Response({
				"success": False, 
				"message": "Bad data."}, status=400)
		answer.save()
		user.save()
		return Response({
			"success": True, 
			"message": message})

	@action(detail=True, methods=['post'], url_path = 'answer', permission_classes=[IsAuthenticated])
	def answer(self, request, pk=None):
		question = self.get_object()
		answer = self.get_serializer(data = request.data)
		if not answer.is_valid():
			return Response({"success": False, "message": "Bad data."}, status=400)

		answer.save(author = request.user, question = question)
		return Response({"success": True, "message": "Answered."})
		
	# def update(self, request, pk):
	# 	pass

	# def partial_update(self, request, pk):
	# 	pass

	def destroy(self, request, pk):
		pass
