from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from executor.models import Worker, Team, Project, Position
from task.models import Task


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_editable = ["first_name", "last_name", "position"]
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (_("Additional info"), {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            _("Additional info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "position",
                )
            },
        ),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "deadline",
        "priority",
        "is_completed",
    ]
    list_filter = ["deadline", "priority", "is_completed"]
    list_editable = ["description", "deadline", "priority", "is_completed"]
    search_fields = ["name"]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "deadline"]
    list_filter = ["name", "deadline"]
    list_editable = ["description", "deadline"]
    search_fields = ["name"]


admin.site.register(Position)
