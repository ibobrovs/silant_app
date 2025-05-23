from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Machine, Maintenance, Claim

class Command(BaseCommand):
    help = 'Создаёт группы и назначает права'

    def handle(self, *args, **kwargs):
        def create_group(name, perms):
            group, created = Group.objects.get_or_create(name=name)
            group.permissions.set(perms)
            group.save()

        view_machine = Permission.objects.get(codename='view_machine')
        add_maintenance = Permission.objects.get(codename='add_maintenance')
        view_maintenance = Permission.objects.get(codename='view_maintenance')
        add_claim = Permission.objects.get(codename='add_claim')
        view_claim = Permission.objects.get(codename='view_claim')

        create_group('Клиент', [view_machine, view_maintenance, add_maintenance, view_claim, add_claim])
        create_group('Сервисная организация', [view_machine, add_maintenance, add_claim])
        create_group('Менеджер', Permission.objects.all())

        self.stdout.write(self.style.SUCCESS('Группы и права созданы.'))
