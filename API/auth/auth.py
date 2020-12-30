from Utilities.Serializers.auth import UserSerializer
from Utilities.functionalities import get_token
from Config.models import PasswordResetKey, User

import datetime

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password


@api_view(['POST',])
def get_confirmation_key(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.send_confirmation()
        return Response({'confirmation_sent':'The confirmation key has been sent to your email'})

    else:
        return Response(data=serializer.errors)

@api_view(['POST',])
def confirm_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        token = str(get_token(user))

        return Response({'token':token})

    else:
        return Response(data=serializer.errors)

@api_view(['POST',])
def get_confirmation_key(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.send_confirmation()
        return Response({'confirmation_sent':'The confirmation key has been sent to your email'})

    else:
        return Response(data=serializer.errors)


@api_view(['POST',])
def login_user(request):    
    try:
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request,username=username,password=password)

        if user is not None:
            token = str(get_token(user))
            return Response({'token':token})
        return Response({'invalid_credentials':True})
    except:
        return Response({'credentials_provided':False})


@api_view(['POST',])
def request_password_reset(request):
    """Send or resend a confirmation key to user's email"""
    data = request.data 
    username = data.get('username',None)

    if username is None:
        return Response({'username_not_provided':'please provide your username'})

    user = User.objects.get(username=username) if User.objects.filter(username=username).exists() else None

    if user is None:
        return Response(data={'invalid_username':'please check if the username is correct'})
    
    password_key_obj, created = PasswordResetKey.objects.get_or_create(user=user)

    if created:
        password_key_obj.save() # It'll generate a new key

    key = password_key_obj.key 

    if not created: 
        # check if user requestes resend early
        if datetime.datetime.now().second -  password_key_obj.key_generated_at.second <= 60:
            return Response({'key_generation_error':'Can\'nt send key : Only send key if it\'s one or more that one minute old'})

    try:
        send_mail(
            'Confirmation_Key',
            f"""Your Confirmation_Key : {key} 
            """,
            "farhansyedain@gmail.com",
            recipient_list=[f'{user.email}']
        )

        return Response({'email_sent_successfull':'Email was sent successfully'})

    except Exception:
        return Response(data={'email_error':f'Could\'nt send the email, try checking weather the email is correct or not '})
     

@api_view(['POST',])
def reset_password(request):
    data = request.data
    username = data.get('username',None)

    if username is None:
        return Response({'username':'please submit the username'})
    
    user = User.objects.get(username=username) if User.objects.filter(username=username).exists() else None

    if user is None:
        return Response({'invalid_username':'the provided username is invalid'})

    password, confirm_password = data.get('password',None), data.get('confirm_password',None)

    if password is None :
        return Response({'password':'Please provide the password'})
    if confirm_password is None:
        return Response({'confirm_password':'Please provide password2'})

    if not password == confirm_password:
        return Response({'password_match':'the two passwords don\'t match'})
    
    try:
        validate_password(password)
    except:
        return Response({'password_valid':'The password does\'nt satisty our validitors'})

    key = data.get('key',None)

    key_obj, created = PasswordResetKey.objects.get_or_create(user=user) 

    if created:
        return Response({'key_not_found':'Please generate the key first'})

    if key == key_obj.key and key is not None:
        user.set_password(password)
        user.save()
        key_obj.delete()

        return Response({'successfull':'password reset was successfull'})

    return Response({'invalid_key':'the key provided was invalid'})
    