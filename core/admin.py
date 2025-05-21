from django.contrib import admin
from .models import *

admin.site.register(Machine)
admin.site.register(Maintenance)
admin.site.register(Claim)
admin.site.register(ModelType)
admin.site.register(EngineModel)
admin.site.register(TransmissionModel)
admin.site.register(DriveAxleModel)
admin.site.register(SteeredAxleModel)
admin.site.register(TOType)
admin.site.register(FailureNode)
admin.site.register(RecoveryMethod)
admin.site.register(ServiceCompany)
