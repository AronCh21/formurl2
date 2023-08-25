from django.contrib import admin
from .models import Beneficiary, Sender, Receipt

admin.site.register(Beneficiary)
admin.site.register(Sender)
admin.site.register(Receipt)