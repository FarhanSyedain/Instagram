from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import authenticate

from Utilities.Serializers.profile import ProfileSerializer, UserSerializer

from Config.models import Profile, User


@api_view(['PUT',])
@permission_classes([IsAuthenticated,])
def update_user_(request):
    user = request.user 
    user_ser = UserSerializer(user,request.data)
    profile_ser = ProfileSerializer(user.profile,request.data) 
    errors = {}
    has_erros = False
    if not user_ser.is_valid():      
        errors = user_ser.errors
        has_erros = True

    if not profile_ser.is_valid():
        errors.update(profile_ser.errors)
        has_erros = True
    
    if has_erros:
        return Response(errors)
            
    #Check for any errors that will occur at the time of saving  
    user_ser.save()
    profile_ser.save()
    #Now Finally save
    user_ser.save(save=True)
    profile_ser.save(save=True)
    return Response({'successfull':'Updated successfully'})


@api_view(['DELETE',])
@permission_classes([IsAuthenticated,])
def delete_user(request):
    user = request.user 
    password = request.data.get('password',None)
    if password is None:
        return Response({'password':'Invalid Password'})

    user = authenticate(request,username=user.username,password=password)
    if user is not None:
        user.delete()
        return Response({'successfull':'User successfully deleted'})
    return Response({'password':'Invalid Password'})
