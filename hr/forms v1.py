# hr/forms.py

from django import forms
from .models import Leave, Employee, Announcement
from .models import CompanyProfile, Department
from .models import Appraisal
from .models import Resignation
from .models import SiteSettings

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['name', 'address', 'phone', 'email', 'website']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']  # Specify the fields to include in the form
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'start_date', 'end_date', 'reason']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'employee': 'Employee',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'reason': 'Reason for Leave',
        }
        help_texts = {
            'reason': 'Please provide a detailed reason for your leave request.',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        employee = cleaned_data.get("employee")

        # Ensure the end date is not before the start date
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be greater than or equal to start date.")

        # Check for overlapping leave requests
        if employee:
            overlapping_leaves = Leave.objects.filter(
                employee=employee,
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exists()
            if overlapping_leaves:
                raise forms.ValidationError("This leave request overlaps with an existing leave.")
        
        # Additional validation for maximum leave duration (e.g., 30 days)
        if start_date and end_date:
            leave_duration = (end_date - start_date).days
            if leave_duration > 30:
                raise forms.ValidationError("Leave duration cannot exceed 30 days.")


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'staff_id', 'first_name', 'last_name', 'email', 'phone', 'department', 'job_title', 'date_joined', 'profile_picture', 'resume']
        widgets = {
            # 'user': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.TextInput(attrs={'readonly': 'readonly'}),
            'staff_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'date_joined': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'user': 'User',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone': 'Phone',
            'job_title': 'Job Title',
            'department': 'Department',
            'date_joined': 'Date Joined',
            'profile_picture': 'Profile Picture',
            'resume': 'Resume',
        }

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name', '').strip().lower()
        last_name = cleaned_data.get('last_name', '').strip().lower()

        if first_name and last_name:
            cleaned_data['user'] = f"{first_name}.{last_name}"

        return cleaned_data


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'title': 'Announcement Title',
            'content': 'Announcement Content',
        }
        help_texts = {
            'content': 'Please provide detailed information for the announcement.',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Announcement.objects.filter(title=title).exists():
            raise forms.ValidationError("An announcement with this title already exists.")
        return title

class AppraisalForm(forms.ModelForm):
    class Meta:
        model = Appraisal
        fields = ['employee', 'score', 'review_date', 'comments']

class ResignationForm(forms.ModelForm):
    class Meta:
        model = Resignation
        fields = ['employee', 'resignation_date', 'reason', 'comments']  # Adjust fields as necessary

    def __init__(self, *args, **kwargs):
        super(ResignationForm, self).__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({'class': 'form-control'})  # Example styling
        self.fields['resignation_date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
        self.fields['reason'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Reason for resignation'})
        self.fields['comments'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Additional comments', 'rows': 3})

class SettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['site_name', 'site_email', 'maintenance_mode']  # Add fields you want to display
        labels = {
            'site_name': 'Website Name',
            'site_email': 'Contact Email',
            'maintenance_mode': 'Enable Maintenance Mode',
        }
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'site_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'maintenance_mode': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
