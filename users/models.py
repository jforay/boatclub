from django.db import models
from boats_and_locations.models import Marina
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
# Create your models here.

#manages creation of users and superusers
class CustomUserManager(BaseUserManager):
    #creating regular user
    def create_user(self,email,password=None,group_name=None, **extra_fields):
        if not email:
            raise ValueError('Email field must be set')

        email = self.normalize_email(email)
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            raise ValueError(f"The group '{group_name}' is not a valid group. ")

        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        user.groups.add(group)
        return user
    

    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        return self.create_user(email,password=password,group_name='Boss', **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customUser_groups',
        blank=True,
        help_text='The groups this user belongs to',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customUser_permissions',
        blank=True,
        help_text='Permissions for this user',
        verbose_name='user permissions',
    )
    first_name = models.CharField(max_length=20,null=True,blank=True)
    last_name = models.CharField(max_length=20,null=True,blank=True)
    home_marina = models.ForeignKey(Marina, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    trained_drivers = models.CharField(max_length=255, null=True, blank=True)
    surf_trained = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def is_member(self):
        return self.groups.filter(name='Member').exists()

    def is_employee(self):
        return self.groups.filter(name__in=['Employee','Manager','Boss']).exists()

    def is_manager(self):
        return self.groups.filter(name__in=['Manager','Boss']).exists()

    def is_boss(self):
        return self.groups.filter(name='Boss').exists()