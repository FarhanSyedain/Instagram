from django.db.models.signals import post_save
from .models import Profile, User

def create_profile(sender,instance,created,*args,**kwargs):
    if created:
        profile, _created = Profile.objects.get_or_create(user=instance)
        if _created:
            profile.save()


post_save.connect(create_profile,User)
        

