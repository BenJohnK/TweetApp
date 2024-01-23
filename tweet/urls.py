from django.urls import path
from .views import RegisterView, LoginView, LogoutView, PostsView, LikePostView, CommentPostView


urlpatterns = [
    path('auth/signup', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('posts/create/', PostsView.as_view({'post': 'create'}), name='create_post'),
    path('posts/get/', PostsView.as_view({'get': 'list'}), name='get_all_posts'),
    path('posts/edit/<int:pk>/', PostsView.as_view({'put': 'update'}), name='edit_post'),
    path('posts/delete/<int:pk>/', PostsView.as_view({'delete': 'destroy'}), name='delete_post'),
    path('posts/<int:post_id>/like', LikePostView.as_view(), name="like_post"),
    path('posts/<int:post_id>/comment', CommentPostView.as_view(), name="comment_post")
]