# hr/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class CompanyProfile(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, default='+123456789')
    email = models.EmailField(unique=True, default='default@example.com')
    website = models.URLField(max_length=200, default='www.company.com')
    established_date = models.DateField(default=timezone.now)
    city = models.CharField(max_length=100, default='City')
    state = models.CharField(max_length=100, default='State')
    country = models.CharField(max_length=100, default='Country')

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  # Added description field
    company = models.ForeignKey(CompanyProfile, null=True, blank=True, on_delete=models.SET_NULL)  # Allow null values

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.CharField(max_length=150, unique=True)  # Use CharField for auto-fill
    staff_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    date_joined = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='Pending')

    def duration(self):
        return (self.end_date - self.start_date).days

    def clean(self):
        # Ensure the end date is not before the start date
        if self.start_date > self.end_date:
            raise ValidationError("End date must be greater than or equal to start date.")

        # Check for overlapping leave requests
        overlapping_leaves = Leave.objects.filter(
            employee=self.employee,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date
        ).exists()
        if overlapping_leaves:
            raise ValidationError("This leave request overlaps with an existing leave.")


class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20)

    def clean(self):
        # Ensure that the end date is not before the start date
        if self.start_date > self.end_date:
            raise ValidationError("End date must be after or on the start date.")
        # Overlapping leave check if necessary
        overlapping_requests = LeaveRequest.objects.filter(
            employee=self.employee,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date
        ).exists()
        if overlapping_requests:
            raise ValidationError("This leave request overlaps with an existing request.")

    def __str__(self):
        return f"{self.leave_type} leave request for {self.employee} from {self.start_date} to {self.end_date}"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')], default='Present', blank=True)

    def save(self, *args, **kwargs):
        if not self.status:
            if self.check_in_time:
                self.status = 'Present'
            else:
                self.status = 'Absent'
        super().save(*args, **kwargs)


class Resignation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    resignation_date = models.DateField()
    reason = models.TextField()
    comments = models.TextField(blank=True, null=True)

    def clean(self):
        # Ensure resignation_date is not in the future
        if self.resignation_date > timezone.now().date():
            raise ValidationError("Resignation date cannot be in the future.")

    def __str__(self):
        return f"{self.employee} resigned on {self.resignation_date}"


class Recruitment(models.Model):
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title


class Appraisal(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    review_date = models.DateField(default=timezone.now)
    comments = models.TextField(blank=True, null=True)  # Optional comments field

    class Meta:
        verbose_name_plural = "Appraisals"

    def __str__(self):
        return f"Appraisal for {self.employee.user.username} on {self.review_date}"
    

class Settings(models.Model):
    setting1 = models.CharField(max_length=255, blank=True, null=True)
    setting2 = models.CharField(max_length=255, blank=True, null=True)
    # Add more fields as necessary
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings: {self.setting1}, {self.setting2}"

class SiteSettings(models.Model):
    maintenance_mode = models.BooleanField(default=False)
    site_name = models.CharField(max_length=255)
    site_email = models.EmailField()
    site_phone = models.CharField(max_length=15)

    def __str__(self):
        return self.site_name
