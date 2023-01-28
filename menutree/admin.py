from django.contrib import admin

from .models import Item


class ItemInline(admin.TabularInline):
    model = Item
    readonly_fields = ['path']
    extra = 0
    verbose_name = 'Дочерний пункт меню'
    verbose_name_plural = 'Дочерние пункты меню'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
    readonly_fields = ['id', 'path']
    list_display = ['id', 'name', 'parent', 'url', 'path']
    ordering = ['path']
