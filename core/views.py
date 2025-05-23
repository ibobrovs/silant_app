from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Machine, Maintenance, Claim


def index(request):
    return render(request, 'core/index.html')

# Список машин
def machine_list(request):
    machines = Machine.objects.all().order_by('shipment_date')
    return render(request, 'core/machine_list.html', {'machines': machines})

# Детали машины
def machine_detail(request, pk):
    machine = get_object_or_404(Machine, pk=pk)
    return render(request, 'core/machine_detail.html', {'machine': machine})

# Аналогично для ТО:
def maintenance_list(request):
    maintenance = Maintenance.objects.all().order_by('date')
    return render(request, 'core/maintenance_list.html', {'maintenance': maintenance})

def maintenance_detail(request, pk):
    item = get_object_or_404(Maintenance, pk=pk)
    return render(request, 'core/maintenance_detail.html', {'item': item})

# И для рекламаций:
def claim_list(request):
    claims = Claim.objects.all().order_by('date')
    return render(request, 'core/claim_list.html', {'claims': claims})

def claim_detail(request, pk):
    item = get_object_or_404(Claim, pk=pk)
    return render(request, 'core/claim_detail.html', {'item': item})


def is_manager(user):
    return user.groups.filter(name='Менеджер').exists()

@user_passes_test(is_manager)
def edit_machine(request, pk):
    ...