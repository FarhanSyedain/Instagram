from rest_framework import serializers

from Config.models import User, Profile
from Utilities.functionalities import valid_username
from PIL import Image

from django.contrib.auth.password_validation import validate_password



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'private', 'phone_number', 'country']
    

    def save(self,save=False,*args,**kwargs):
        if save:
            self.instance.save()

        private = self.initial_data.get('private',None)

        if not private is None:
            if private == 'False':
                self.instance.private = False
            else:
                self.instance.private = True

        bio = self.initial_data.get('bio',False)
        if bio:
            self.instance.bio = bio
        
        number = self.initial_data.get('phone_number',False)
        if number:
            self.instance.phone_number = number
        
        country = self.validated_data.get('country',False)
        if country:
            self.instance.country = country
        
        profile_picture = self.validated_data.get('profile_picture',False)
        clear_profile = self.initial_data.get('clear_profile',False)

        if clear_profile:
            if bool(self.instance.profile_picture):
                path = self.instance.profile_picture.path
                self.instance.profile_picture.delete()

        if profile_picture:
            if bool(self.instance.profile_picture): # removet he previous profile picture , (if any)
                path = self.instance.profile_picture.path
                self.instance.profile_picture.delete()

            self.instance.profile_picture = profile_picture


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email','first_name','last_name','email']
    

    def save(self,save=False,*args,**kwargs):
        username = self.initial_data.get('username',False)

        if save:
            try:
                self.instance.save()
            except Exception as e:
                if not valid_username(username):
                    raise serializers.ValidationError({'username_ununique':'The username is already taken or been registerd'})
                raise e

        confirm_password = self.initial_data.get('confirm_password',None)
        password = self.initial_data.get('password',None)

        if password is not None or confirm_password is not None:
            if password != confirm_password:
                raise serializers.ValidationError({'passwords':'The two passwords don\'t match'})
            try:
                validate_password(password)
            except:
                raise serializers.ValidationError({'password_invalid':'the given password doesn\'t satisfy our validation'})

            self.instance.set_password(password)
    
        first_name = self.validated_data.get('first_name',False)
        last_name = self.validated_data.get('last_name',False)
        email = self.validated_data.get('email',False)

        if first_name:
            self.instance.first_name = first_name
        
        if last_name:
            self.instance.last_name = last_name

        if email:
            self.instance.email = email
        
        if not self.instance.username == username:
           if not valid_username(username):
               raise serializers.ValidationError({'username_ununique':'The username is already taken or been registerd'})

        if username:
            self.instance.username = username
        

#class FollowersSerilizer(serializers.ModelSerializer):
