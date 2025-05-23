from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import (Machine, Maintenance, Claim, ModelType, EngineModel, TransmissionModel, 
                     DriveAxleModel, SteeredAxleModel, TOType, ServiceCompany, FailureNode, RecoveryMethod)
from django.http import HttpResponseForbidden
from .forms import MaintenanceForm

def index(request):
    return render(request, 'core/index.html')


# ------------------------
#     МАШИНЫ
# ------------------------
@login_required
def machine_list(request):
    user = request.user

    if user.groups.filter(name='Клиент').exists():
        machines = Machine.objects.filter(client=user)
    elif user.groups.filter(name='Сервисная организация').exists():
        machines = Machine.objects.filter(service_company=user)
    elif user.groups.filter(name='Менеджер').exists():
        machines = Machine.objects.all()
    else:
        machines = Machine.objects.none()


    machines = Machine.objects.all().order_by('shipment_date')

    # Фильтры
    model = request.GET.get('model')
    engine = request.GET.get('engine')
    trans = request.GET.get('transmission')
    steer_axle = request.GET.get('steered_axle')
    drive_axle = request.GET.get('drive_axle')

    if model:
        machines = machines.filter(model__id=model)
    if engine:
        machines = machines.filter(engine_model__id=engine)
    if trans:
        machines = machines.filter(transmission_model__id=trans)
    if drive_axle:
        machines = machines.filter(drive_axle_model__id=drive_axle)
    if steer_axle:
        machines = machines.filter(steered_axle_model__id=steer_axle)

    context = {
        'machines': machines,
        'models': ModelType.objects.all(),
        'engines': EngineModel.objects.all(),
        'transmissions': TransmissionModel.objects.all(),
        'drive_axles': DriveAxleModel.objects.all(),
        'steered_axles': SteeredAxleModel.objects.all(),
        'selected': request.GET
    }
    return render(request, 'core/machine_list.html', context)

@login_required
def machine_detail(request, pk):
    machine = get_object_or_404(Machine, pk=pk)
    return render(request, 'core/machine_detail.html', {'machine': machine})

def machine_search(request):
    query = request.GET.get('serial')
    machine = None
    not_found = False

    if query:
        machine = Machine.objects.filter(serial_number=query).first()
        if not machine:
            not_found = True

    return render(request, 'core/machine_search.html', {
        'machine': machine,
        'query': query,
        'not_found': not_found,
    })


# ------------------------
#     ТЕХОБСЛУЖИВАНИЕ
# ------------------------
@login_required
def maintenance_list(request):
    maintenance = Maintenance.objects.all().order_by('date')

    to_type = request.GET.get('to_type')
    serial = request.GET.get('serial')
    service = request.GET.get('service')

    if to_type:
        maintenance = maintenance.filter(type__id=to_type)
    if serial:
        maintenance = maintenance.filter(machine__serial_number__icontains=serial)
    if service:
        maintenance = maintenance.filter(service_company__id=service)

    context = {
        'maintenance': maintenance,
        'to_types': TOType.objects.all(),
        'services': ServiceCompany.objects.all(),
        'selected': request.GET
    }
    return render(request, 'core/maintenance_list.html', context)

@login_required
def maintenance_detail(request, pk):
    item = get_object_or_404(Maintenance, pk=pk)
    return render(request, 'core/maintenance_detail.html', {'item': item})

@login_required
def add_maintenance(request):
    user = request.user

    if not user.groups.filter(name__in=['Клиент', 'Сервисная организация']).exists():
        return HttpResponseForbidden("У вас нет прав на добавление ТО.")

    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)

            if user.groups.filter(name='Клиент').exists() and maintenance.machine.client != user:
                return HttpResponseForbidden("Это не ваша техника.")

            if user.groups.filter(name='Сервисная организация').exists() and maintenance.machine.service_company != user:
                return HttpResponseForbidden("Это не ваша техника.")

            maintenance.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm()

    return render(request, 'core/add_maintenance.html', {'form': form})

# ------------------------
#     РЕКЛАМАЦИИ
# ------------------------
@login_required
def claim_list(request):
    claims = Claim.objects.all().order_by('date')

    node = request.GET.get('failure_node')
    method = request.GET.get('recovery_method')
    service = request.GET.get('service')

    if node:
        claims = claims.filter(failure_node__id=node)
    if method:
        claims = claims.filter(recovery_method__id=method)
    if service:
        claims = claims.filter(service_company__id=service)

    context = {
        'claims': claims,
        'nodes': FailureNode.objects.all(),
        'methods': RecoveryMethod.objects.all(),
        'services': ServiceCompany.objects.all(),
        'selected': request.GET
    }
    return render(request, 'core/claim_list.html', context)
@login_required

def claim_detail(request, pk):
    item = get_object_or_404(Claim, pk=pk)
    return render(request, 'core/claim_detail.html', {'item': item})


# ------------------------
#     Роли (пример)
# ------------------------

def is_manager(user):
    return user.groups.filter(name='Менеджер').exists()

@user_passes_test(is_manager)
def edit_machine(request, pk):

    ...

def is_client(user):
    return user.groups.filter(name='Клиент').exists()

@user_passes_test(is_client)
def client_dashboard(request):
    ...

