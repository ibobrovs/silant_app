from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import Machine, Maintenance, Claim

        def create_group(name, perms=[]):
            group, created = Group.objects.get_or_create(name=name)
            group.permissions.clear()
            for perm in perms:
                group.permissions.add(perm)

        if not Group.objects.exists():
            ct_machine = ContentType.objects.get_for_model(Machine)
            ct_to = ContentType.objects.get_for_model(Maintenance)
            ct_claim = ContentType.objects.get_for_model(Claim)

            create_group('Клиент', [
                Permission.objects.get(codename='view_machine'),
                Permission.objects.get(codename='view_maintenance'),
                Permission.objects.get(codename='add_maintenance'),
                Permission.objects.get(codename='view_claim'),
                Permission.objects.get(codename='add_claim'),
            ])
            create_group('Сервисная организация', [
                Permission.objects.get(codename='view_machine'),
                Permission.objects.get(codename='add_maintenance'),
                Permission.objects.get(codename='add_claim'),
            ])
            create_group('Менеджер', Permission.objects.all())
