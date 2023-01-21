from django.db import models
from django.utils.crypto import get_random_string

from core.models import User


class TgUser(models.Model):
    tg_chat_id = models.BigIntegerField(verbose_name="telegram chat id", unique=True)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.PROTECT, null=True, blank=True,
                             default=None)
    tg_username = models.CharField(max_length=32, verbose_name="tg username", null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=12)

    class Meta:
        verbose_name = "Telegram пользователь"
        verbose_name_plural = "Telegram пользователи"

    def set_verification_code(self) -> str:
        code = get_random_string(12)
        self.verification_code = code
        self.save()
        return code
