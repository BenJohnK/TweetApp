from django.contrib import admin
from .models import CustomUser, Post, Like, Comment, FriendRequest, Friendship

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(FriendRequest)
admin.site.register(Friendship)
