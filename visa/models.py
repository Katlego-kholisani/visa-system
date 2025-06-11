from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

#user Model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('applicant', 'Applicant'),
        ('officer', 'Officer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='applicant')

    # Add custom related_name to resolve conflicts
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="visa_user_groups",
        related_query_name="visa_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="visa_user_permissions",
        related_query_name="visa_user",
    )

"""
DO NOT FORGET TO ADD GROUP AND PERMISSIONS HERE!!!
"""

#employer model
class Employer(models.Model):
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name

#residence model
class ResidenceDetails(models.Model):
    address= models.TextField()
    duration_months = models.PositiveIntegerField()
    sponsor_name = models.CharField(max_length=100)
    sponsor_relationship = models.CharField(max_length=100)

    def __str__(self):
        return self.address

#Visa Application Model
class VisaApplication(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    VISA_TYPES = (
        ('work', 'Work'),
        ('residence', 'Residence'),
    )

    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visa_applications')
    visa_type = models.CharField(max_length=20, choices=VISA_TYPES)
    passport_number = models.CharField(max_length=50)
    country_of_origin = models.CharField(max_length=100)
    employer = models.ForeignKey(Employer, on_delete=models.SET_NULL, null=True, blank=True)
    residence_details= models.ForeignKey(ResidenceDetails, on_delete=models.SET_NULL, null=True, blank=True)
    submission_date = models.DateTimeField(default= timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    def __str__(self):
        return f"{self.passport_number}  -  {self.visa_type}"


class ApplicationDocument(models.Model):
    visa_application = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50) # Employment Letter le di Lease Agreements
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateField(auto_now_add=True)


class StatusChangeLog(models.Model):
    visa_application = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name='status_log')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=50)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    changed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.visa_application} changed from {self.old_status} to {self.new_status}"
