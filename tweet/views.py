from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.middleware.csrf import rotate_token
from .serializers import (
    UserSerializer,
    PostSerializer,
    LikeSerializer,
    CommentSerializer,
    FriendRequestSerializer,
)
from .models import Post, Like, Comment, FriendRequest, CustomUser, Friendship, Follow
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from .custom_permissions import IsOriginalUser
from django.shortcuts import get_object_or_404
from django.db.models import Q


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
        post_id = self.kwargs["post_id"]
        post = Post.objects.get(id=post_id)
        serializer.save(post=post, user=self.request.user)


class CommentPostView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs["post_id"]
        post = Post.objects.get(id=post_id)
        serializer.save(post=post, user=self.request.user)


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, to_user_id):
        to_user = get_object_or_404(CustomUser, id=to_user_id)
        friend_request = FriendRequest(from_user=request.user, to_user=to_user)
        friend_request.save()
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RespondToFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, friend_request_id, action):
        friend_request = get_object_or_404(
            FriendRequest,
            id=friend_request_id,
            to_user=request.user,
            is_accepted_or_rejected=False,
        )

        if action == "accept":
            print("here")

            Friendship.objects.create(
                user1=request.user, user2=friend_request.from_user
            )
            friend_request.is_accepted_or_rejected = True
            friend_request.save()
            return Response(
                {"detail": "Friend request accepted."}, status=status.HTTP_200_OK
            )
        elif action == "reject":
            friend_request.is_accepted_or_rejected = True
            return Response(
                {"detail": "Friend request rejected."}, status=status.HTTP_200_OK
            )


class RemoveFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, friend_id, *args, **kwargs):
        friendship = Friendship.objects.filter(
            (Q(user1=request.user) & Q(user2_id=friend_id))
            | (Q(user2=request.user) & Q(user1_id=friend_id))
        )
        friendship.delete()
        return Response({"detail": "Friend removed."}, status=status.HTTP_200_OK)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        to_user = get_object_or_404(CustomUser, id=user_id)

        if request.user == to_user:
            return Response(
                {"detail": "Cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Follow.objects.filter(follower=request.user, following=to_user).exists():
            return Response(
                {"detail": "You are already following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Follow.objects.create(follower=request.user, following=to_user)
        return Response(
            {"detail": "User followed successfully."}, status=status.HTTP_200_OK
        )


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id, *args, **kwargs):
        to_user = get_object_or_404(CustomUser, id=user_id)

        if request.user == to_user:
            return Response(
                {"detail": "Cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow = Follow.objects.filter(follower=request.user, following=to_user)
        if not follow.exists():
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow.delete()
        return Response(
            {"detail": "User unfollowed successfully."}, status=status.HTTP_200_OK
        )
