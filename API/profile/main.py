from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from Config.models import User, Profile, Follow, Following, Posts
from Utilities.functionalities import follow_user as _follow_user , unfollow_user as _unfollow_user, unsend_follow_request as UFR, follows
from Utilities.Serializers.profile import ProfileSerializer, UserSerializer

from django.contrib.auth import authenticate


@api_view(['GET'])
def get_user_info(request):
    
    """
    Returns follower count , following count , is_private, posts_count , weather user follows the profile visiter (The request sender) \n
    and weather user is followd by the visiter
    """

    visiter = request.user.profile

    user = request.data.get('user',None)

    if user is None:
        return Response(data={'user':'This field is required'})
    
    user , created = User.objects.get_or_create(username=user)

    if created: # If a user with the provided username didn't exist
        return Response(status=404,data={'user':'Invalid username'})

    private = user.profile.private

    if private: 
        private = follows(visiter,user)
    
    followers_obj = Follow.objects.get_or_create(user=user.profile)
    following_obj = Following.objects.get_or_create(user=user.profile)

    followers_count = followers_obj.followers.count()
    following_count = following_obj.following.count()

    posts_count = Posts.all_posts.count()

    follows_visiter = follows(user,visiter.user)
    is_followed_by_visiter = follows(visiter.user,user)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def follow_user(request):
    user = request.user
    to_be_followed = request.data.get('follow',None)

    if to_be_followed is None:
        return Response({'follow':'This field is required'})
    
    to_be_followed, created = User.objects.get_or_create(username=to_be_followed)

    if created:
        return Response({'follow':'The username doesn\'nt exist'})
    
    try:
        _ = _follow_user(to_be_followed,user)
        
        if _ is 0: # If a follw request is sent
            return Response({'Follow Request Sent':'A follow request has been sent to the user'})

        if _ is 1: # If user is followed
            return Response({'User Followed':'The user has been followed successfully'})

    except:
        return Response({'Error':'There was an error from our side'},status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def unfollow_user(request):
    user = request.user
    to_be_unfollowed = request.data.get('unfollow',None)

    if to_be_unfollowed is None:
        return Response({'unfollow':'This field is required'})
    
    to_be_unfollowed, created = User.objects.get_or_create(username=to_be_unfollowed)

    if created:
        return Response({'unfollow':'Invalid username'})
    
    try:
        _ = _unfollow_user(to_be_unfollowed,user)

        return Response({'User Unfollowed'})

    except:
        return Response({'Error':'There was an error from our side'},status=500) 


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def unsend_followRequest(request):
    user = request.user
    unsend_to = request.data.get('Unsend',None)

    if unsend_to is None:
        return Response({'Unsend':'This field is required'})

    unsend_to , created = User.objects.get_or_create(username=unsend_to)

    if created:
        return Response({'Unsend':'Invaalid username'})
    
    try:
        _ = UFR(user,unsend_to)

        return Response({'Request Unsend':'The follow request has been unsent'})
    
    except:
        return Response({'Error':'There was an error from our side'},status=500) 
    

@api_view(['PUT',])
@permission_classes([IsAuthenticated,])
def update_user(request):
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


class GetFollowers(ListAPIView):

    """
    Returns the users who follw user,along with weather the visiter — the one who sent api request — follows them or they follow him/her
    """

    permission_classes = [IsAuthenticated,]
    serializer_class = None

    def get_queryset(self,*args,**kwargs):
        user = self.request.data.get('user',None)
        
        if user is None:
            raise ValidationError(detail={'user':'This field is required — send as a query_param'})
        
        user, created = User.objects.get_or_create(username=user)

        if created:
            raise ValidationError(detail={'user':'Invalid username'})
            
        visiter = self.request.user
        if user.profile.is_private:
            followers_obj, created = Follow.objects.get_or_create(user=user.profile)
            if not followers_obj.followers.filter(username=user).exists():
                raise ValidationError(detail={'Private account':'This account is private , follow the user to access the followers'})
        
        
   
class GetFollowing(ListAPIView):

    """
    Returns the users a user follows,along with weather the visiter — the one who sent api request — follows them or they follow him/her
    """
