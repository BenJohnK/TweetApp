from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.middleware.csrf import rotate_token
from .serializers import UserSerializer, PostSerializer, LikeSerializer, CommentSerializer
from .models import Post, Like, Comment
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from .custom_permissions import IsOriginalUser


# Create your views here.


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    def post(self, request):
        form = AuthenticationForm(request, data=request.data)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            rotate_token(request)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class PostsView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOriginalUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikePostView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)
        serializer.save(post=post, user=self.request.user)
    

class CommentPostView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)
        serializer.save(post=post, user=self.request.user)

