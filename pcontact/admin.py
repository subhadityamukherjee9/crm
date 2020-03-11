from django.contrib import admin
from .forms import CustomerForm, CompanyAssociationForm
#from mezzanine.utils.admin import SingletonAdmin
from .models import Contacts,CompanyAssociation,InsttitueAssociation,Company,Institute,Tags

class SystemAdmin(admin.ModelAdmin):
    form = CustomerForm
    inlines=()

class CompanyAdmin(admin.ModelAdmin):
    form = CompanyAssociationForm
    inlines=()

admin.site.register(Contacts, SystemAdmin)
admin.site.register(CompanyAssociation, CompanyAdmin)
admin.site.register(InsttitueAssociation)
admin.site.register(Company)
admin.site.register(Institute)
admin.site.register(Tags)
