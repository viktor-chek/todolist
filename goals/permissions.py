from rest_framework import permissions

from goals.models import BoardParticipant


class BoardPermissions(permissions.BasePermission):
    """Разграничение доступа для доски"""
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class GoalPermissions(permissions.BasePermission):
    """Разграничение доступа для цели"""
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.category.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.category.board,
            role__in=[
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer,
            ],
        ).exists()


class CommentPermissions(permissions.BasePermission):
    """Разграничение доступа для комментария"""
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.goal.category.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.goal.category.board,
            role__in=[
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer,
                BoardParticipant.Role.reader,
            ],
        ).exists()


class GoalCategoryPermissions(permissions.BasePermission):
    """Разграничение доступа для категории"""
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.board,
            role__in=[
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer,
            ],
        ).exists()
