# GVLDash does not use a database. However, the django auth system tries to save the last logged in time.
# Therefore, disable the save signal as described here:
# http://stackoverflow.com/questions/1057149/django-users-and-authentication-from-external-source

from django.contrib.auth.models import update_last_login, user_logged_in, AbstractUser
user_logged_in.disconnect(update_last_login)

class GVLUser(AbstractUser):
    USERNAME_FIELD = "username"

    def save (self):
        """saving to DB disabled"""
        pass

    objects = None # we cannot really use this w/o local DB
    username = None

    def get_group_permissions (self):
        """If you don't make your own permissions module,
           the default also will use the DB. Throw it away"""
        return [] # likewise with the other permission defs

    def get_and_delete_messages (self):
        """Messages are stored in the DB. Darn!"""
        return []