from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from rest_framework import views
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SignupView(views.APIView):
	serializer_class = SignupSerializer

	def post(self,request):
		serializer = SignupSerializer(data=request.data)
		if not serializer.is_valid():
			return Response({"success":False, "message": serializer.errors})

		serializer.save()
		return Response({"success": True, "message": "Successful signed up."})


class UserListView(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserListSerializer

class UserDetailView(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserDetailSerializer

class ProfileView(generics.GenericAPIView):
	serializer_class = ProfileSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = User.objects.get(pk= self.request.user.pk)
		return queryset

	def get(self,request):
		user = self.get_queryset()
		serializer = ProfileSerializer(user)
		return Response(serializer.data)

	def post(self,request):
		user = self.get_queryset()
		serializer = ProfileSerializer(user, data=request.data)
		if not serializer.is_valid():
			return Response({"success":False, "message": serializer.erros}, status=400)
		serializer.save()
		return Response({"success": True, "message": "Successful updated."})

