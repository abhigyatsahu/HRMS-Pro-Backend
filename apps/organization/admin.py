from django.contrib import admin

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "email",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "legal_name",
        "email",
        "phone",
    )

    ordering = (
        "name",
    )

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )