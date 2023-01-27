from django.contrib import admin
from .models import Item, Menu


class ItemInline(admin.StackedInline):
    model = Item
    readonly_fields = ['path']
    extra = 1
    verbose_name = 'Дочерний пункт меню'
    verbose_name_plural = 'Дочерние пункты меню'

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
    list_display = ['id', 'name', 'menu', 'parent', 'path', 'url']
    readonly_fields = ['path']
    # TODO menu field from parent or parent from menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
