from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.dc import Message
from todolist.settings import TG_TOKEN
from bot.tg.bot_manager import ManageBot

from bot.tg.client import TgClient


class Command(BaseCommand):
    help = 'Start bot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(TG_TOKEN)
        self.manage = ManageBot()

    def handle(self, *args, **options):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(message=item.message)

    def handle_message(self, message: Message):
        tg_user, created = TgUser.objects.get_or_create(tg_chat_id=message.from_.id, tg_username=message.from_.username)

        if created:
            self.tg_client.send_message(message.chat.id, f'Приветствую, {message.from_.first_name}!')

        if not tg_user.user:
            self.manage.dont_verified_user(tg_user)
            self.tg_client.send_message(message.chat.id,
                                        f"Подтвердите, пожалуйста, свой аккаунт на сайте chekus.ga\n"
                                        f"Для подтверждения необходимо ввести код из следующего сообщения")
            self.tg_client.send_message(message.chat.id, f"{tg_user.verification_code}")
        else:
            self.handle_message_for_verified_user(message, tg_user)

    def handle_message_for_verified_user(self, message: Message, tg_user: TgUser):
        if message.text.startswith('/'):
            res = self.manage.check_command(message, tg_user)
        else:
            res = self.manage.check_status(message, tg_user)
        self.tg_client.send_message(message.chat.id, res)
