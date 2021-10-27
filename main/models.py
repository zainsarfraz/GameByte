from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class UserDetails(models.Model):
    age = models.IntegerField(default=18)
    bio = models.CharField(max_length=400,default="N/A")
    profile_pic = models.ImageField(upload_to="",null=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self) -> str:
        return self.user_id.email