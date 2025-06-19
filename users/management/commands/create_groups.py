from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
from users.models import CustomUser

class Command(BaseCommand):
    help = 'creates user groups and asssigns permissions to groups'

    def handle(self, *args, **kwargs):
        boss_group, created = Group.objects.get_or_create(name='Boss')
        manager_group, created = Group.objects.get_or_create(name='Manager')
        employee_group, created = Group.objects.get_or_create(name='Employee')
        member_group, created = Group.objects.get_or_create(name='Member')

        user_content_type = ContentType.objects.get_for_model(CustomUser)

        employee_permissions =[
            Permission.objects.get_or_create(codename='view_schedule',name='Can view boat schedule', content_type=user_content_type)[0]
        ]
        employee_group.permissions.set(employee_permissions)
        manager_permissions = list(employee_group.permissions.all())
        
        manager_specific_permissions = [
            Permission.objects.get_or_create(codename='add_boat',name='Can add boat to fleet',content_type=user_content_type)[0],
            Permission.objects.get_or_create(codename='edit_boat',name='Can edit boat',content_type=user_content_type)[0],
        ]

        manager_permissions.extend(manager_specific_permissions)

        manager_group.permissions.set(manager_permissions)

        boss_permissions = list(manager_group.permissions.all())
        
        boss_specific_permissions = [
            Permission.objects.get_or_create(codename='add_user', name='Can add user', content_type=user_content_type)[0],
            Permission.objects.get_or_create(codename='edit_user',name='Can edit user',content_type=user_content_type)[0],
            Permission.objects.get_or_create(codename='delete_user',name='Can delete user',content_type=user_content_type)[0],
            Permission.objects.get_or_create(codename='view_user',name='Can view user',content_type=user_content_type)[0],
            ]
        
        boss_permissions.extend(boss_specific_permissions)

        boss_group.permissions.set(boss_permissions)

        self.stdout.write(self.style.SUCCESS('Groups and permissions created successfully!'))