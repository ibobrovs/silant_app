from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import (Machine, Maintenance, Claim, ModelType, EngineModel, TransmissionModel, 
                     DriveAxleModel, SteeredAxleModel, TOType, ServiceCompany, FailureNode, RecoveryMethod)
from django.http import HttpResponseForbidden
from .forms import MaintenanceForm, ClaimForm, MachineForm
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import MachineSerializer, MaintenanceSerializer, ClaimSerializer
from django_filters.rest_framework import DjangoFilterBackend



def index(request):
    return render(request, 'core/index.html')


# ------------------------
#     МАШИНЫ
# ------------------------
machines = Machine.objects.filter(is_active=True).order_by('shipment_date')

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

@login_required
def add_machine(request):
    user = request.user

    # Только для менеджеров
    if not user.groups.filter(name='Менеджер').exists():
        return HttpResponseForbidden("У вас нет прав на добавление машин.")

    if request.method == 'POST':
        form = MachineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('machine_list')
    else:
        form = MachineForm()

    return render(request, 'core/add_machine.html', {'form': form})

def machine_search(request):
    query = request.GET.get('serial')
    machine = None
    not_found = False

    if query:
        machine = Machine.objects.filter(serial_number=query, is_active=True).first()
        if not machine:
            not_found = True

    return render(request, 'core/machine_search.html', {
        'machine': machine,
        'query': query,
        'not_found': not_found,
    })

@login_required
def edit_machine(request, pk):
    user = request.user
    if not user.groups.filter(name='Менеджер').exists():
        return HttpResponseForbidden("Нет доступа")

    machine = get_object_or_404(Machine, pk=pk)

    if request.method == 'POST':
        form = MachineForm(request.POST, instance=machine)
        if form.is_valid():
            form.save()
            return redirect('machine_detail', pk=pk)
    else:
        form = MachineForm(instance=machine)

    return render(request, 'core/edit_machine.html', {'form': form, 'machine': machine})

@login_required
def delete_machine(request, pk):
    user = request.user
    if not user.groups.filter(name='Менеджер').exists():
        return HttpResponseForbidden("Нет прав")

    machine = get_object_or_404(Machine, pk=pk)
    machine.is_active = False
    machine.save()
    return redirect('machine_list')

# ------------------------
#     ТЕХОБСЛУЖИВАНИЕ
# ------------------------
maintenance = Maintenance.objects.filter(is_active=True).order_by('date')


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

@login_required
def maintenance_detail(request, pk):
    item = get_object_or_404(Maintenance, pk=pk)
    return render(request, 'core/maintenance_detail.html', {'item': item})


@login_required
def edit_maintenance(request, pk):
    user = request.user
    maintenance = get_object_or_404(Maintenance, pk=pk)

    if user.groups.filter(name='Клиент').exists() and maintenance.machine.client != user:
        return HttpResponseForbidden("Вы не можете редактировать ТО.")

    if user.groups.filter(name='Сервисная организация').exists() and maintenance.machine.service_company != user:
        return HttpResponseForbidden("Вы не можете редактировать ТО.")

    if not user.groups.filter(name__in=['Клиент', 'Сервисная организация', 'Менеджер']).exists():
        return HttpResponseForbidden("Нет прав доступа.")

    if request.method == 'POST':
        form = MaintenanceForm(request.POST, instance=maintenance)
        if form.is_valid():
            form.save()
            return redirect('maintenance_detail', pk=pk)
    else:
        form = MaintenanceForm(instance=maintenance)

    return render(request, 'core/edit_maintenance.html', {'form': form, 'item': maintenance})

# ------------------------
#     РЕКЛАМАЦИИ
# ------------------------
claims = Claim.objects.filter(is_active=True).order_by('date')

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

@login_required
def add_claim(request):
    user = request.user

    if not user.groups.filter(name__in=['Клиент', 'Сервисная компания']).exists():
        return HttpResponseForbidden("У вас нет прав на добавление рекламации.")

    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)

            if user.groups.filter(name='Клиент').exists() and claim.machine.client != user:
                return HttpResponseForbidden("Это не ваша техника.")
            if user.groups.filter(name='Сервисная компания').exists() and claim.machine.service_company != user:
                return HttpResponseForbidden("Это не ваша техника.")

            claim.save()
            return redirect('claim_list')
    else:
        form = ClaimForm()

    return render(request, 'core/add_claim.html', {'form': form})

login_required
def edit_claim(request, pk):
    user = request.user
    claim = get_object_or_404(Claim, pk=pk)

    if user.groups.filter(name='Клиент').exists() and claim.machine.client != user:
        return HttpResponseForbidden("Вы не можете редактировать чужую рекламацию.")

    if user.groups.filter(name='Сервисная организация').exists() and claim.machine.service_company != user:
        return HttpResponseForbidden("Вы не можете редактировать чужую рекламацию.")

    if not user.groups.filter(name__in=['Клиент', 'Сервисная организация', 'Менеджер']).exists():
        return HttpResponseForbidden("Нет прав доступа.")

    if request.method == 'POST':
        form = ClaimForm(request.POST, instance=claim)
        if form.is_valid():
            form.save()
            return redirect('claim_detail', pk=pk)
    else:
        form = ClaimForm(instance=claim)

    return render(request, 'core/edit_claim.html', {'form': form, 'item': claim})

# ------------------------
#     Роли (пример)
# ------------------------

def is_manager(user):
    return user.groups.filter(name='Менеджер').exists()

def is_client(user):
    return user.groups.filter(name='Клиент').exists()

@user_passes_test(is_client)
def client_dashboard(request):
    ...

class MachineAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        machines = Machine.objects.filter(is_active=True)
        serializer = MachineSerializer(machines, many=True)
        return Response(serializer.data)
    
class MaintenanceAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        maintenance = Maintenance.objects.filter(is_active=True)
        serializer = MaintenanceSerializer(maintenance, many=True)
        return Response(serializer.data)
    
class ClaimAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        claims = Claim.objects.filter(is_active=True)
        serializer = ClaimSerializer(claims, many=True)
        return Response(serializer.data)
    
class MachineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Machine.objects.filter(is_active=True)
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['model', 'engine_model', 'transmission_model', 'drive_axle_model', 'steered_axle_model']

class MaintenanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Maintenance.objects.filter(is_active=True)
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'machine__serial_number', 'service_company']

class ClaimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Claim.objects.filter(is_active=True)
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['failure_node', 'recovery_method', 'service_company']
