from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from rest_framework.response import Response

class TagViewset(viewsets.GenericViewSet):
	lookup_field = 'slug'
	def get_serializer_class(self):
		if self.action == 'list':
			return TagListSerializer
		elif self.action == 'retrieve':
			return TagDetailSerializer
		return EmptySerializer

	def get_queryset(self):
		queryset = Tag.objects.all()
		return queryset

	def get_object(self, slug):
		tag = Tag.objects.filter(slug=slug)
		return tag

	def list(self,request):
		queryset = self.get_queryset()
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, slug):
		tag = self.get_object(slug)
		tagged_questions = self.get_serializer(tag, many=True)
		return Response(tagged_questions.data)

