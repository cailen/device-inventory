from django.contrib import admin
from django.contrib.contenttypes.generic import GenericStackedInline

from reversion import VersionAdmin

from inventory.devices.models import Ipad


class IpadAdmin(VersionAdmin):
    list_display = ['lender', 'lendee', 'status','condition', 'updated_at']

admin.site.register(Ipad, IpadAdmin)