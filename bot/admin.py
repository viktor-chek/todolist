from django.contrib import admin

from bot.models import TgUser


@admin.register(TgUser)
class UserAdmin(admin.ModelAdmin):
    search_fields = ["tg_username", "user"]
    list_display = ["tg_username", "verification_code", "tg_chat_id", "user"]