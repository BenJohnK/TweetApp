from rest_framework import serializers
from .models import CustomUser, Post, Like, Comment, FriendRequest, Follow, Friendship
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)
    number_of_posts = serializers.SerializerMethodField()
    number_of_followers = serializers.SerializerMethodField()
    number_of_following = serializers.SerializerMethodField()
    number_of_friends = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "password",
            "password_confirmation",
            "phone_number",
            "number_of_posts",
            "number_of_followers",
            "number_of_following",
            "number_of_friends",
        ]
        extra_kwargs = {"password": {"write_only": True}, "email": {"required": True}}

    def validate(self, data):
        if "password" in data:
            if data["password"] != data["password_confirmation"]:
                raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirmation", None)
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def get_number_of_posts(self, obj):
        posts = Post.objects.filter(user=obj)
        return posts.count()

    def get_number_of_followers(self, obj):
        return Follow.objects.filter(following=obj).count()

    def get_number_of_following(self, obj):
        return Follow.objects.filter(follower=obj).count()

    def get_number_of_friends(self, obj):
        friendships = Friendship.objects.filter(Q(user1=obj) | Q(user2=obj))
        return friendships.count()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post", "timestamp"]
        read_only_fields = ["user", "post"]


class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "post", "text", "timestamp"]
        read_only_fields = ["user", "post"]


class PostSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "text",
            "user",
            "time_stamp",
            "likes_count",
            "liked_by",
            "comments",
            "comments_count",
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked_by(self, obj):
        likes = Like.objects.filter(post=obj)
        liked_users = likes.values("user")
        user_ids = [like["user"] for like in liked_users]
        liked_users_data = CustomUser.objects.filter(id__in=user_ids)
        return CustomUserSerializer(liked_users_data, many=True).data

    def get_comments_count(self, obj):
        return obj.comments.count()


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ["id", "from_user", "to_user", "is_accepted_or_rejected", "timestamp"]
