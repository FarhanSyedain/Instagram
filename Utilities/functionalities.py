from rest_framework.authtoken.models import Token

from Config.models import User, ConfirmationKey,datetime, Profile, Follow, Following

def get_token(user,generate=True):
    """
    ?Generate : If True generates a token for a user not having that.
    """

    if Token.objects.filter(user=user).exists():
        return Token.objects.get(user=user)
    
    if generate:
        token = Token(user=user)
        token.save()

        return token


def valid_username(username):
    """Returns True if the username is not taken , otherwise False"""
    
    if User.objects.filter(username=username).exists():
        return False
    
    if ConfirmationKey.objects.filter(username=username).exists():
        key = ConfirmationKey.objects.get(username=username)
        if not datetime.datetime.now().second - key.key_generated_at.sceond >= 3600:
            return False
        
    return True


def follow_user(follow_whom,by_whom):

    """
    Follows a user and returns 1 if successfully followd or 0 if a follow request is sent to the user
    """

    if not isinstance(follow_whom,User) and not isinstance(by_whom,User):
        raise Exception('Follow whom and by whom should be User instances')

    follow_whom_profile = follow_user.profile
    by_whom_profile = by_whom.profile
    
    follow_obj, created = Follow.objects.get_or_create(user=follow_whom_profile)
    following_obj, created = Following.objects.get_or_create(user=by_whom)

    if follow_whom.private:
        follow_obj.followRequests.add(by_whom_profile)
        following_obj.followRequestsSent.add(follow_whom)
        
        return 0

    follow_obj.followers.add(by_whom)
    following_obj.following.add(follow_whom)
    follow_obj.save()
    following_obj.save()

    return 1


def unfollow_user(unfollow_whom, by_whom):
    
    """
    Unfollows a user and returns True
    """
    
    if not isinstance(unfollow_user,User) and not isinstance(by_whom,User):
        raise Exception('Unfollow whom and by whom should be User instances')
    
    unfollow_whom_profile = unfollow_whom.profile
    by_whom_profile = by_whom.profile

    follow_obj, created = Follow.objects.get_or_create(user=unfollow_whom_profile)
    following_obj, created = Following.objects.get_or_create(user=by_whom)

    follow_obj.followers.remove(by_whom_profile)
    following_obj.following.remove(unfollow_whom_profile)

    follow_obj.save()
    following_obj.save()

    return True


def unsend_follow_request(unsend_from,unsend_to): 
    
    """
    Unsends a previously sent follow request and returns True
    """
    
    if not isinstance(unsend_from,User) and not isinstance(unsend_to,User):
        raise Exception('unsend_from and unsend_to should be User instances')

    unsend_from = unsend_from.profile
    unsend_to = unsend_to.profile

    follow_obj, created = Follow.objects.get_or_create(user=unsend_to)
    following_obj, created = Following.objects.get_or_create(user=unsend_from)

    follow_obj.FollowRequests.remove(unsend_from)
    following_obj.FollowRequestsSent.remove(unsend_to)

    return True


def follows(who,whom):
    """
    Returns true if who follows whom
    parmas : who = User object ; whom = user object
    """

    if not isinstance(who,User) or not isinstance(whom,User):
        raise Exception({'Who and Whom should be User instanes'})
    who = who.profile

    following_obj = Following.objects.get_or_create(user=who)

    if following_obj.following.filter(username=whom.username):
        return True
    
    return False


