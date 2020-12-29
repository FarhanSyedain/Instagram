import binascii
import os
import json
import random
import datetime

from django.db import models
from django.contrib.auth.models import User, AbstractUser

class PasswordResetKey(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    key = models.CharField(max_length=20,null=True,blank=True)
    key_generated_at = models.DateTimeField(blank=True,null=True)
    initial_request_sent = models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        if self.key is None or not self.is_valid():
            self.key = binascii.hexlify(os.urandom(20)).decode()
            self.key_generated_at = datetime.datetime.now() 

    def is_valid(self):
        """Checks weather the key is still valid or not"""
        if datetime.datetime.now().second - datetime.timedelta(self.key_generated_at).seconds >= 600:
            return True
        return False 
    
    def regenerate_key(self):
        #The time period between generation of keys should be >= 60 sceonds
        if datetime.datetime.now().second - datetime.timedelta(self.key_generated_at).seconds >= 60: 
            self.key = binascii.hexlify(os.urandom(20)).decode()
            self.key_generated_at = datetime.datetime.now() 
            self.save()
            return True
        return False


class ConfirmationKey(models.Model):
    key = models.CharField(max_length=20,blank=True)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    confirmation_key = models.CharField(max_length=10,null=True,blank=True)
    key_generated_at = models.DateTimeField(blank=True,null=True)
    initial_request_sent = models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        if self.key is None or len(self.key)== 0 or not self.is_valid():
            self.key = binascii.hexlify(os.urandom(20)).decode()
            self.confirmation_key = binascii.hexlify(os.urandom(8)).decode()
            self.key_generated_at = datetime.datetime.now() 
        
        super().save(*args,**kwargs)
      
    def is_valid(self):
        """Returns weather the key is still valid or not"""
        if datetime.datetime.now().second - datetime.timedelta(self.key_generated_at).seconds >= 600:
            return True
        return False 

    
    def regenerate_key(self):
        #The time period between generation of keys should be >= 60 sceonds
        if datetime.datetime.now().second - datetime.timedelta(self.key_generated_at).seconds >= 60: 
            self.confirmation_key = binascii.unhexlify(os.urandom(random.randint(4,8)))
            self.key_generated_at = datetime.datetime.now() 
            self.save()
            return True
        return False
        
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    profile_picture = models.ImageField(blank=True,null=True,upload_to="Data/Users/Profiles")
    bio = models.TextField(blank=True,null=True)
    private = models.BooleanField(default=False)
    profile_updated = models.DateTimeField(auto_now=True)
    following = models.ManyToManyField('self',blank=True)
    followers = models.ManyToManyField('self',blank=True)
    phone_number = models.IntegerField(blank=True)
    country = models.CharField(max_length=25,blank=True,null=True)
    followRequestsSend = models.ManyToManyField('self',blank=True)
    followRequests = models.ManyToManyField('self',blank=True)


class Post(models.Model):
    people_tagged = models.ManyToManyField(Profile,blank=True)
    post = models.FileField(upload_to="Data/Users/Posts")
    tags = models.TextField(blank=True)
    mentions = models.TextField(blank=True)
    disciption = models.TextField(blank=True)
    location = models.CharField(max_length=100,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField('Comment',blank=True)


class Posts(models.Model):
    user = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True)
    all_posts = models.ManyToManyField(Post,blank=True,related_name='posts')
    tagged = models.ManyToManyField(Post,blank=True,related_name='tagged_in')
    bookmarks = models.ManyToManyField(Post,blank=True,related_name='bookmarked_in')


class Comment(models.Model):
    body = models.TextField(blank=True)
    by = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)


class CommentReply(models.Model):
    body = models.TextField(blank=True)
    by = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    parent = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True)


class Story(models.Model):
    post = models.FileField(upload_to="Data/Users/Stories") 
    date = models.DateTimeField(auto_now_add=True)
    by = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)