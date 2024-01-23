from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=12)

    class Meta:
        db_table = "custom_user"

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",
        blank=True,
        help_text="Specific permissions for this user.",
    )


class Post(models.Model):
    text = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(CustomUser, related_name="likes", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "post"]


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sent_requests"
    )
    to_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="received_requests"
    )
    is_accepted_or_rejected = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class Friendship(models.Model):
    user1 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user1_friends"
    )
    user2 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user2_friends"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user1", "user2"]
