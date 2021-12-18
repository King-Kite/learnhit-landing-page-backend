from django.contrib import admin
from .models import Subscriber

class SubscriberAdmin(admin.ModelAdmin):
    '''
        Admin View for Subscriber
    '''
    list_display = ('email',)
    list_filter = ('email',)
    search_fields = ('email',)

admin.site.register(Subscriber, SubscriberAdmin)
