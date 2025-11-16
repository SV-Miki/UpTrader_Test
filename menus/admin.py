from django.contrib import admin

from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    fields = ("title", "parent", "named_url", "url", "order")
    extra = 1
    raw_id_fields = ("parent",)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "title")
    inlines = (MenuItemInline,)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("title", "menu", "parent", "order")
    list_filter = ("menu",)
    search_fields = ("title", "named_url", "url")
    raw_id_fields = ("parent",)
