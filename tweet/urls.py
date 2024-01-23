from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    PostsView,
    LikePostView,
    CommentPostView,
    SendFriendRequestView,
    RespondToFriendRequestView,
    RemoveFriendView,
    FollowUserView,
    UnfollowUserView,
    UserProfileView,
)


urlpatterns = [
    path("auth/signup/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("posts/create/", PostsView.as_view({"post": "create"}), name="create_post"),
    path("posts/get/", PostsView.as_view({"get": "list"}), name="get_all_posts"),
    path(
        "posts/edit/<int:pk>/", PostsView.as_view({"put": "update"}), name="edit_post"
    ),
    path(
        "posts/delete/<int:pk>/",
        PostsView.as_view({"delete": "destroy"}),
        name="delete_post",
    ),
    path("posts/<int:post_id>/like/", LikePostView.as_view(), name="like_post"),
    path(
        "posts/<int:post_id>/comment/", CommentPostView.as_view(), name="comment_post"
    ),
    path(
        "friends/add/<int:to_user_id>/",
        SendFriendRequestView.as_view(),
        name="send_friend_request",
    ),
    path(
        "friends/accept/<int:friend_request_id>/<str:action>/",
        RespondToFriendRequestView.as_view(),
        name="respond_to_friend_request",
    ),
    path(
        "friends/remove/<int:friend_id>/",
        RemoveFriendView.as_view(),
        name="remove_friend",
    ),
    path("followers/follow/<int:user_id>/", FollowUserView.as_view(), name="follow"),
    path(
        "followers/unfollow/<int:user_id>/", UnfollowUserView.as_view(), name="unfollow"
    ),
    path(
        "user/profile/<int:pk>/",
        UserProfileView.as_view({"get": "retrieve"}),
        name="get_user_profile",
    ),
    path(
        "user/edit-profile/<int:pk>/",
        UserProfileView.as_view({"put": "update"}),
        name="update_user_profile",
    ),
]
