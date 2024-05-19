from django.db import models
from django.http import Http404


class DashboardManager(models.Manager):
    def current(self, request, *args, **kwargs):
        return self.filter(owner__user=request.user, *args, **kwargs).first()


class ProjectManager(models.Manager):
    def current_or_none(self, pk, request, *args, **kwargs):
        return self.filter(pk=pk, members__user=request.user, *args, **kwargs).first()

    def current_or_404(self, pk, request, *args, **kwargs):
        project = self.current_or_none(pk, request, *args, **kwargs)
        if not project:
            raise Http404('Не найдено ни одного проекта по вашему запросу.')
        return project


class ProjectMemberManager(models.Manager):
    def current_or_none(self, project_pk, request, *args, **kwargs):
        return self.filter(project__pk=project_pk, project__members__user=request.user, *args, **kwargs).first()

    def current_or_404(self, project_pk, request, *args, **kwargs):
        member = self.current_or_none(project_pk, request, *args, **kwargs)
        if not member:
            raise Http404('Не найдено ни одного проекта/участника проекта по вашему запросу.')
        return member


class StatusManager(models.Manager):
    def current_or_none(self, project_pk, request, *args, **kwargs):
        return self.filter(project__pk=project_pk, project__members__user=request.user, *args, **kwargs).first()

    def current_or_404(self, project_pk, request, *args, **kwargs):
        status = self.current_or_none(project_pk, request, *args, **kwargs)
        if not status:
            raise Http404('Не найдено ни одного проекта/статуса проекта по вашему запросу.')
        return status


class MarkerManager(models.Manager):
    def current_or_none(self, project_pk, request, *args, **kwargs):
        return self.filter(project__pk=project_pk, project__members__user=request.user, *args, **kwargs).first()

    def current_or_404(self, project_pk, request, *args, **kwargs):
        marker = self.current_or_none(project_pk, request, *args, **kwargs)
        if not marker:
            raise Http404('Не найдено ни одного проекта/маркера проекта по вашему запросу.')
        return marker


class GroupManager(models.Manager):
    def current_or_none(self, project_pk, request, *args, **kwargs):
        return self.filter(project__pk=project_pk, project__members__user=request.user, *args, **kwargs).first()

    def current_or_404(self, project_pk, request, *args, **kwargs):
        group = self.current_or_none(project_pk, request, *args, **kwargs)
        if not group:
            raise Http404('Не найдено ни одного(-ой) проекта/группы проекта по вашему запросу.')
        return group


class DashboardProjectManager(models.Manager):
    def current_or_none(self, project_pk, request, *args, **kwargs):
        return self.filter(
            project__pk=project_pk,
            dashboard__owner__user=request.user,
            *args, **kwargs
        ).first()

    def current_or_404(self, project_pk, request, *args, **kwargs):
        dashboard_project = self.current_or_none(project_pk, request, *args, **kwargs)
        if not dashboard_project:
            raise Http404('Не найдено ни одного проекта по вашему запросу.')
        return dashboard_project


class TaskManager(models.Manager):
    def current_or_none(self, project_pk, request, *args, **kwargs):
        return self.filter(project__pk=project_pk, project__members__user=request.user, *args, **kwargs).first()

    def current_or_404(self, project_pk, request, *args, **kwargs):
        task = self.current_or_none(project_pk, request, *args, **kwargs)
        if not task:
            raise Http404('Не найдено ни одного(-ой) проекта/задачи проекта по вашему запросу.')
        return task

    def bulk_update_status(self, current_status, new_status):
        tasks = self.filter(status=current_status)
        for task in tasks:
            task.status = new_status
        return self.bulk_update(tasks, ['status'])


class CommentManager(models.Manager):
    def current_or_none(self, project_pk, task_pk, request, *args, **kwargs):
        return self.filter(
            task__project_pk=project_pk,
            task__pk=task_pk,
            task__project__members__user=request.user,
            *args, **kwargs
        ).first()

    def current_or_404(self, project_pk, request, *args, **kwargs):
        comment = self.current_or_none(project_pk, request, *args, **kwargs)
        if not comment:
            raise Http404('Не найдено ни одного(-ой) проекта/задачи/коментария к задаче по вашему запросу.')
        return comment
