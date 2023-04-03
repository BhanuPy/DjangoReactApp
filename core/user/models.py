import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.db import models

from core.abstract.models import AbstractManager, AbstractModel

# Create your models here.

class UserManager(BaseUserManager, AbstractManager):
    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404  
        
    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a "User" with an email, phone number, username and password."""
        
        if username is None:
            raise TypeError("Users must have a username.")
        
        if email is None:
            raise TypeError("Users must have an email.")
        
        if password is None:
            raise TypeError("User must have an email.")
        

        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)


        return user
    

    def create_superuser(self, username, email, password=None, **kwargs):
        """Create and return a "User" with superuser(admin) permissions."""
        
        if username is None:
            raise TypeError("SuperUsers must have a username.")
        
        if email is None:
            raise TypeError("SuperUsers must have an email.")
        
        if password is None:
            raise TypeError("SuperUser must have an email.")
        

        user = self.create_user(username,email, password, **kwargs)
        user.is_superuser  = True
        user.is_staff = True
        # user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        # user.set_password(password)
        user.save(using=self._db)

        return user


        return user
 
class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    
    public_id = models.UUIDField(db_index=True, unique=True,default=uuid.uuid4, editable=False)
    username = models.CharField(db_index=True, max_length=255,unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)

    # bio = models.TextField(null=True)
    # avatar = models.ImageField(null=True, blank=True, upload_to=user_directory_path)

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"
    
    @property
    def name(self):
        return f"{self.first_name}  {self.last_name}"
    

