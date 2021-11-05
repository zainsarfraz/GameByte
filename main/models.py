from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class UserDetails(models.Model):
    age = models.IntegerField(default=18)
    bio = models.CharField(max_length=400,default="N/A")
    profile_pic = models.ImageField(upload_to="",null=True)
    cover_pic = models.ImageField(upload_to="",null=True)
    company = models.CharField(max_length=100,default="N/A")
    education = models.CharField(max_length=100,default="N/A")
    rank_star = models.IntegerField(default=0)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self) -> str:
        return self.user_id.email