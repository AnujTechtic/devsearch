from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
    name = models.CharField(max_length = 200, blank= True, null=True)
    email = models.EmailField(max_length = 200, blank=True, null = True)
    username = models.CharField(max_length = 200, blank= True, null=True)
    location = models.CharField(max_length = 200, blank= True, null=True)
    header = models.CharField(max_length = 200, blank = True, null = True)
    bio = models.TextField(blank = True, null = True)
    profile = models.ImageField(null = True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    social_github = models.CharField(max_length = 200, blank= True, null=True)
    social_twitter = models.CharField(max_length = 200, blank= True, null=True)
    social_youtube = models.CharField(max_length = 200, blank= True, null=True)
    social_linkedin = models.CharField(max_length = 200, blank= True, null=True)
    social_website = models.CharField(max_length = 200, blank= True, null=True)
    id = models.UUIDField(default = uuid.uuid4, unique= True, primary_key= True, editable= False)
    created = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return str(self.username)


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True, blank= True)
    name = models.CharField(max_length = 200, blank= True, null=True)
    description = models.TextField(blank = True, null = True)
    id = models.UUIDField(default = uuid.uuid4, unique= True, primary_key= True, editable= False)
    created = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return str(self.name)

# @receiver(post_save, sender= Profile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user= user,
            username = user.username,
            email = user.email,
            name  = user.first_name,
        )

def deleteUser(sender, instance,  **kwargs):
    print("Deleted the User")


post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, Profile)