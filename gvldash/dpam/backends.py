import pam

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from customauth.models import GVLUser

class PAMBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        service = getattr(settings, 'PAM_SERVICE', 'login')
        if pam.authenticate(username, password, service=service):
            try:
                user = GVLUser(id=username, username=username)
            except:
                user = GVLUser(id=username, username=username, password='not stored here')
                user.set_unusable_password()

                if getattr(settings, 'PAM_IS_SUPERUSER', False):
                    user.is_superuser = True

                if getattr(settings, 'PAM_IS_STAFF', user.is_superuser):
                    user.is_staff = True

#                 user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return GVLUser(id=user_id, username=id)
        except User.DoesNotExist:
            return None
