from goals.models import Goal, GoalCategory


class BotState:
    default = 0
    choose_cat = 1
    create_goal = 2

    def __init__(self, state):
        self.state = state

    def set_state(self, state):
        self.state = state


STATE = BotState(state=BotState.default)


class ManageBot:
    def __init__(self):
        self.storage_for_create = {}

    def get_category(self, tg_user):
        categories = GoalCategory.objects.filter(board__participants__user=tg_user.user, is_deleted=False)
        if categories.count() > 0:
            return [f'{item.id}) {item.title}'for item in categories]
        else:
            return ['Список категорий пуст']

    def dont_verified_user(self, tg_user):
        tg_user.set_verification_code()
        tg_user.save(update_fields=['verification_code'])

    def check_command(self, message, tg_user) -> str:
        if message.text == '/goals':
            goals = self.get_goals(tg_user)
            if goals:
                res = 'Ваши цели:\n' + '\n'.join(goals)
            else:
                res = 'У вас ещё нет созданных целей'
        elif message.text == '/create':
            STATE.set_state(BotState.choose_cat)
            categories = self.get_category(tg_user)
            res = f"Выберите категорию в которой хотите создать цель:\n" + '\n'.join(categories)
        elif message.text == '/site':
            res = 'chekus.ga'
        elif message.text == '/cancel':
            STATE.set_state(BotState.default)
            self.storage_for_create = {}
            res = "Операция отменена"
        else:
            res = "Такой команды нет"
        return res

    def check_status(self, message, tg_user):
        if STATE.state == BotState.default:
            res = 'Введите какую-нибудь команду'
        elif STATE.state == BotState.choose_cat:
            res = self.input_category(message, tg_user)
        elif STATE.state == BotState.create_goal:
            res = self.create_goal(message)
        else:
            res = 'Что-то пошло не так, попробуйте заново'
        return res

    def input_category(self, message, tg_user):
        category = GoalCategory.objects.filter(
            title__exact=message.text,
            board__participants__user=tg_user.user,
            is_deleted=False
        ).first()
        if category:
            self.storage_for_create['category'] = category
            res = f'Вы выбрали категорию "{category.title}"\nВведите название цели:'
            STATE.set_state(BotState.create_goal)
        else:
            res = 'Такой категории нет'
        return res

    def create_goal(self, message):
        cat = self.storage_for_create['category']
        Goal.objects.create(user=cat.user, title=message.text, category=cat)
        res = "Цель создана!"
        STATE.set_state(BotState.default)
        return res


    def get_goals(self, tg_user):
        goals = Goal.objects.filter(category__board__participants__user=tg_user.user).exclude(status=Goal.Status.archived)
        return [f'{item.id}) {item.title}' for item in goals]
