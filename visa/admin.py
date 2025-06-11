from django.contrib import admin
from django.contrib import admin
from .models import (
    User,
    Employer,
    ResidenceDetails,
    VisaApplication,
    ApplicationDocument,
    StatusChangeLog
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_staff')


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'contact_email')


@admin.register(ResidenceDetails)
class ResidenceDetailsAdmin(admin.ModelAdmin):
    list_display = ('address', 'duration_months', 'sponsor_name')


@admin.register(VisaApplication)
class VisaApplicationAdmin(admin.ModelAdmin):
    list_display = ('passport_number', 'visa_type', 'status', 'submission_date')
    list_filter = ('visa_type', 'status')


@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'visa_application', 'uploaded_at')


@admin.register(StatusChangeLog)
class StatusChangeLogAdmin(admin.ModelAdmin):
    list_display = ('visa_application', 'old_status', 'new_status', 'changed_by', 'changed_at')
