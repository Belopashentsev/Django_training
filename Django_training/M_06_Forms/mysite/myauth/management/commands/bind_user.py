# команда для связи пользователя с группами и правами
from django.contrib.auth.models import User, Permission, Group
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(pk=4)
        group, created = Group.objects.get_or_create(
            name="profile_manager",
        )
        permission_profile = Permission.objects.get(
            codename="view_profile",
        )
        permission_logentry = Permission.objects.get(
            codename="view_logentry",
        )

        # добавления резрешения к группе
        group.permissions.add(permission_profile) # view_profile будет связан с profile_manager

        # добавление пользователя в группу
        user.groups.add(group) # связь юзера

        # связать пользователя и разрешение напрямую
        user.user_permissions.add(permission_logentry)

        group.save()
        user.save()