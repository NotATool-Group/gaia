# create a Login and Register view, only API
# create a function to check if the user is authenticated
# create a function to logout the user

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer
from .service import verify_activation_token


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivateView(APIView):
    @transaction.atomic
    def get(self, request, token):
        if verify_activation_token(token):
            return HttpResponseRedirect(settings.BASE_URL)
        return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
