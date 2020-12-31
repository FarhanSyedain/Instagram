from rest_framework import serializers

from Config.models import User, ConfirmationKey, Profile

from django.contrib.auth.password_validation import validate_password 
from django.core.mail import send_mail

from Utilities.functionalities import valid_username

class UserSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(style={'input_type':'password'},write_only=True)
    user_email = serializers.CharField(style={'input_type':'email'},write_only=True)
    
    class Meta:
        model = User
        fields = ['user_email','username','confirm_password','password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        confirmation_key = self.initial_data.get('confirmation_key',None)

        if user_info:= self.check_details():
            username , email = user_info
            password = self.validated_data['password']

            try:
                key = ConfirmationKey.objects.get(username=username,email=email)
            except:# If key obj for the user isn't found
                raise serializers.ValidationError({'key_old_or_not_generated':'Either the key has\'nt been generated or key is old' })
                
            if key.confirmation_key == confirmation_key:# weather key is invalid or not
                if key.is_valid(): # weather key is old or not
                    user = User(username=username,email=email)
                    user.set_password(password)
                    user.save()
                    key.delete()
                    
                    return user

                raise serializers.ValidationError({'key_old':'The key is old now , try regenerating'}) 

            raise serializers.ValidationError({'key_invalid':'key is invalid'}) 
                    

    def check_details(self):
        """
        Returns True if user can be created with provided detials, and raises errors if provided details are invalid and/or don't satisfy 
        conditions
        
        Key_id : id of the Confirmation_key object. 
        """

        key_id = self.initial_data.get('key_id',None) 
        password, confirm_password = self.validated_data['password'], self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'password_match':'Passwords don\'t match'})

        try:
            validate_password(password) # Run password through password validitors 
        except Exception:
            raise serializers.ValidationError({'password_valid':"The password does'nt satisfy our password guildlines"})

        username , email = self.validated_data['username'], self.validated_data['user_email']

        #Raise an error if a user differnt user is trying to register user with same username
        if ConfirmationKey.objects.filter(username=username).exists(): 
            obj = ConfirmationKey.objects.get(username=username)

            if obj.email != email: 
                if not valid_username(username):
                    if obj.key != key_id :
                        raise serializers.ValidationError({'username_being_registerd':'Another user has already taken the username though not confirmed'}) 
                
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'unique_email':'The email is already taken'})
        
        return username,email
    
    def send_confirmation(self,resend=False):
        if user_info := self.check_details():
            
            username, email = user_info    
            confirmation_key_obj,created = ConfirmationKey.objects.get_or_create(username=username)
            confirmation_key_obj.email = email
            
            confirmation_key_obj.save() # save the creatd obj
            confirmation_key = confirmation_key_obj.confirmation_key
            key_valid_till = confirmation_key_obj.key_valid_till

            if not resend:
                if confirmation_key_obj.initial_request_sent:
                    raise serializers.ValidationError({'confirmation_already_sent':'confirmation_has_already_been_sent'})
                else:
                    confirmation_key_obj.initial_request_sent = True
                    confirmation_key_obj.save()

            try:
                send_mail(
                    'Confirmation_Key',
                    f"""Your Confirmation_Key : {confirmation_key} 
                    Valid Till = {key_valid_till}
                    """,
                    "farhansyedain@gmail.com",
                    recipient_list=[f'{email}']
                )

            except Exception as e:
                raise serializers.ValidationError({'email_error':f'Could\'nt send the email, try checking weather the email is correct or not {e} '})
    
    def resend_confirmation(self):
        if user_info := self.check_details():
            username, email = user_info   
            confirmation_key_obj = ConfirmationKey().objects.get_or_create(username=username,email=email)

            if confirmation_key_obj.regenerate_key.regenerate_key():
                self.send_confirmation(resend=True)
                return True
                
            raise serializers.ValidationError({'regeneration_regected':"Can't regenerate the key : regeneraion can take place only after 1 minute"})