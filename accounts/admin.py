from django.contrib import admin

from .models import *




class OrderAdmin(admin.ModelAdmin):

    actions = ['mark_delivered']

    def mark_delivered(self, request, queryset):
        queryset.update(status='Delivered')

    mark_delivered.short_description = "Mark selected orders as Delivered"


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(Tag)