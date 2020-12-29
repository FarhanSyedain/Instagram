from rest_framework.authtoken.models import Token


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
