from django.db import models
from core.models import User


class Board(models.Model):
    """Модель доски"""
    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(
        verbose_name="Название",
        max_length=255
    )
    is_deleted = models.BooleanField(
        verbose_name="Удалена",
        default=False
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего обновления"
    )


class BoardParticipant(models.Model):
    """Модель участника доски"""
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    editable_choices = Role.choices
    editable_choices.pop(0)

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants"
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants"
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль",
        choices=Role.choices,
        default=Role.owner
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего обновления"
    )


class GoalCategory(models.Model):
    """Модель категории"""
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(
        verbose_name="Название",
        max_length=255
    )
    user = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.PROTECT
    )
    is_deleted = models.BooleanField(
        verbose_name="Удалена",
        default=False
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего обновления"
    )
    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="categories"
    )


class Goal(models.Model):
    """Модель цели"""
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="goals",
        on_delete=models.PROTECT
    )
    category = models.ForeignKey(
        GoalCategory,
        verbose_name="Категория",
        on_delete=models.PROTECT
    )
    title = models.CharField(
        verbose_name="Заголовок",
        max_length=255
    )
    description = models.TextField(
        verbose_name="Описание",
        null=True,
        blank=True,
        default=None
    )
    due_date = models.DateField(
        verbose_name="Дата выполнения",
        null=True,
        blank=True,
        default=None
    )
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус",
        choices=Status.choices,
        default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет",
        choices=Priority.choices,
        default=Priority.medium
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего обновления"
    )


class GoalComment(models.Model):
    """Модель комментария"""
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    user = models.ForeignKey(
        User,
        verbose_name="Автор",
        related_name="goal_comments",
        on_delete=models.PROTECT
    )
    goal = models.ForeignKey(
        Goal,
        verbose_name="Цель",
        related_name="goal_comments",
        on_delete=models.PROTECT
    )
    text = models.TextField(
        verbose_name="Текст"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего обновления"
    )
