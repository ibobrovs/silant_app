from django.db import models
from django.contrib.auth.models import User

class Reference(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class ModelType(Reference): pass
class EngineModel(Reference): pass
class TransmissionModel(Reference): pass
class DriveAxleModel(Reference): pass
class SteeredAxleModel(Reference): pass
class TOType(Reference): pass
class FailureNode(Reference): pass
class RecoveryMethod(Reference): pass
class ServiceCompany(Reference): pass

# Машина
class Machine(models.Model):
    serial_number = models.CharField(max_length=100)
    model = models.ForeignKey(ModelType, on_delete=models.SET_NULL, null=True)
    engine_model = models.ForeignKey(EngineModel, on_delete=models.SET_NULL, null=True)
    engine_serial = models.CharField(max_length=100)
    transmission_model = models.ForeignKey(TransmissionModel, on_delete=models.SET_NULL, null=True)
    transmission_serial = models.CharField(max_length=100)
    drive_axle_model = models.ForeignKey(DriveAxleModel, on_delete=models.SET_NULL, null=True)
    drive_axle_serial = models.CharField(max_length=100)
    steered_axle_model = models.ForeignKey(SteeredAxleModel, on_delete=models.SET_NULL, null=True)
    steered_axle_serial = models.CharField(max_length=100)
    supply_contract = models.CharField(max_length=255)
    shipment_date = models.DateField()
    customer = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    additional_equipment = models.TextField(blank=True)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='machines_as_client')
    service_company = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='machines_as_service')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.model} SN: {self.serial_number}"

# ТО
class Maintenance(models.Model):
    type = models.ForeignKey(TOType, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    operating_hours = models.IntegerField()
    order_number = models.CharField(max_length=100)
    order_date = models.DateField()
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.SET_NULL, null=True)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

# Рекламации
class Claim(models.Model):
    date = models.DateField()
    operating_hours = models.IntegerField()
    failure_node = models.ForeignKey(FailureNode, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    recovery_method = models.ForeignKey(RecoveryMethod, on_delete=models.SET_NULL, null=True)
    parts_used = models.TextField()
    recovery_date = models.DateField()
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def downtime(self):
        return (self.recovery_date - self.date).days
    