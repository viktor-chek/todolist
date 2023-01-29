from enum import Enum
from enum import auto

from goals.models import GoalCategory
from goals.models import Goal


class BotState(Enum):
    """Переключатель статуса бота"""
    default = auto(), "Бездействие"
    choose_cat = auto(), "Выбор категории"
    create_goal = auto(), "Создание цели"


class ManageBot:
    """Менеджер телеграм бота"""
    def __init__(self):
        self.storage_for_create = {}
        self.state = BotState.default

    def get_category(self, tg_user):
        """Функция отдает категории пользователя"""
        categories = GoalCategory.objects.filter(
            board__participants__user=tg_user.user, is_deleted=False)
        if categories.count() > 0:
            return [f'{item.id}) {item.title}' for item in categories]
        else:
            return ['Список категорий пуст']

    def dont_verified_user(self, tg_user):
        """Верификация пользователя"""
        tg_user.set_verification_code()
        tg_user.save(update_fields=['verification_code'])

    def check_command(self, message, tg_user) -> str:
        """Проверка вводимого текста в боте"""
        if message.text == '/goals':
            goals = self.get_goals(tg_user)
            if goals:
                res = 'Ваши цели:\n' + '\n'.join(goals)
            else:
                res = 'У вас ещё нет созданных целей'
        elif message.text == '/create':
            self.state = BotState.choose_cat
            categories = self.get_category(tg_user)
            res = f"Выберите категорию в которой хотите создать цель:\n" + '\n'.join(
                categories)
        elif message.text == '/site':
            res = 'chekus.ga'
        elif message.text == '/cancel':
            self.state = BotState.default
            self.storage_for_create = {}
            res = "Операция отменена"
        else:
            res = "Такой команды нет"
        return res

    def check_status(self, message, tg_user):
        """Функция проверяет статус бота,
        исходя из статуса возвращает разный месседж пользователю"""
        match self.state:
            case BotState.default:
                res = 'Введите какую-нибудь команду'
            case BotState.choose_cat:
                res = self.input_category(message, tg_user)
            case BotState.create_goal:
                res = self.create_goal(message)
            case _:
                res = 'Что-то пошло не так, попробуйте заново'
        return res

    def input_category(self, message, tg_user):
        """Функция обрабатывает статус 'ввода категории (choose_cat)' бота"""
        category = GoalCategory.objects.filter(
            title__exact=message.text,
            board__participants__user=tg_user.user,
            is_deleted=False
        ).first()
        if category:
            self.storage_for_create['category'] = category
            res = f'Вы выбрали категорию "{category.title}"\nВведите название цели:'
            self.state = BotState.create_goal
        else:
            res = 'Такой категории нет'
        return res

    def create_goal(self, message):
        """Функция обрабатывает статус создание цели (create_goal) бота"""
        cat = self.storage_for_create['category']
        Goal.objects.create(user=cat.user, title=message.text, category=cat)
        res = "Цель создана!"
        self.state = BotState.default
        return res

    def get_goals(self, tg_user):
        """Получение всех доступных целей пользователя"""
        goals = Goal.objects.filter(
            category__board__participants__user=tg_user.user).exclude(
            status=Goal.Status.archived)
        return [f'{item.id}) {item.title}' for item in goals]
