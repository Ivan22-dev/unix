from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
           
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user 



class Account(AbstractBaseUser):
    #Enum initialize start
    MENTOR = 'mentor'
    STUDENT = 'student'
    NONE = 'none'
    REDOVNI = 'redovni'
    IZVANREDNI='izvanredni'
    ROLES=(
        (MENTOR, _('mentor')),
        (STUDENT, _('student')),
    )
    STATUSES=(
        (NONE, _('none')),
        (REDOVNI, _('redovni')),
        (IZVANREDNI, _('izvanredni')),
    )
    #Enum initialize end
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                = models.CharField(max_length=30,unique=True)
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    role= models.CharField(_('role'), default=STUDENT, choices=ROLES, max_length=20)
    status= models.CharField(_('status'), default=NONE, choices=STATUSES, max_length=20)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True




class Items(models.Model):
    name=models.CharField(max_length=255,unique=True)
    code=models.CharField(max_length=16,primary_key=True,unique=True )
    program=models.CharField(max_length=300)
    points=models.IntegerField()
    sem_redovni=models.IntegerField()
    sem_izvanredni=models.IntegerField()
    #Enum initialize start
    DA = 'da'
    NE = 'ne'
    IZBORNI=(
        (DA, _('da')),
        (NE, _('ne')),
    )
    #Enum initialize end
    izborni=models.CharField(_('izborni'), default=NE, choices=IZBORNI, max_length=10)
 

class Enrollment(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE,default="")
    itemid=models.ForeignKey(Items, on_delete=models.CASCADE,default="")
    #Enum initialize start
    POLOŽENO = 'položeno'
    NEPOLOŽENO = 'nepoloženo'
    IZBOR=(
        (POLOŽENO, _('položeno')),
        (NEPOLOŽENO, _('nepoloženo')),
    )
    #Enum initialize end
    status=models.CharField(_('status'), default=NEPOLOŽENO, choices=IZBOR, max_length=20)
    class Meta:
        unique_together = [['user_id','itemid']]


