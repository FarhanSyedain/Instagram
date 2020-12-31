from rest_framework.authtoken.models import Token

from Config.models import User, ConfirmationKey,datetime

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



    
