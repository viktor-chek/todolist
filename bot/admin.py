from django.contrib import admin

from bot.models import TgUser


@admin.register(TgUser)
class TgAdmin(admin.ModelAdmin):
    search_fields = ["username", "email", "first_name", "last_name"]
    list_display = ["username", "email", "first_name", "last_name"]
    list_filter = ["is_staff", "is_active", "is_superuser"]
    exclude = ["password"]
    readonly_fields = ["date_joined", "last_login"]