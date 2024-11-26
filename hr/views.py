# hr/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Employee, Attendance, Leave, Appraisal, Announcement, 
    Resignation, CompanyProfile, Department, LeaveRequest, 
    Recruitment, SiteSettings, Settings
)
from .forms import (
    LeaveForm, EmployeeForm, AnnouncementForm, ResignationForm,
    CompanyProfileForm, DepartmentForm, AppraisalForm, SettingsForm
)
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.http import require_POST 
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Recruitment List View
class RecruitmentListView(ListView):
    model = Recruitment
    template_name = 'hr/recruitment_list.html'

# Profile View
class ProfileView(View):
    def get(self, request):
        return render(request, 'hr/profile.html')

# Edit Profile View
class EditProfileView(View):
    def get(self, request):
        employee = get_object_or_404(Employee, user=request.user)
        form = EmployeeForm(instance=employee)
        return render(request, 'hr/edit_profile.html', {'form': form})

    def post(self, request):
        employee = get_object_or_404(Employee, user=request.user)
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        return render(request, 'hr/edit_profile.html', {'form': form})

# Home View
def home(request):
    return render(request, 'hr/home.html')

# Dashboard View
def dashboard(request):
    context = {
        'total_employees': Employee.objects.count(),
        'total_leaves': Leave.objects.count(),
        'total_announcements': Announcement.objects.count(),
    }
    return render(request, 'hr/dashboard.html', context)

# Employee List View
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'hr/employee_list.html', {'employees': employees})

# Employee Detail View
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'hr/employee_detail.html', {'employee': employee})

# Employee Create/Edit View
class EmployeeCreateEditView(View):
    template_name = 'hr/employee_form.html'
    
    def get(self, request, pk=None):
        if pk:
            employee = get_object_or_404(Employee, pk=pk)
            form = EmployeeForm(instance=employee)
        else:
            form = EmployeeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk=None):
        if pk:
            employee = get_object_or_404(Employee, pk=pk)
            form = EmployeeForm(request.POST, request.FILES, instance=employee)
        else:
            form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Employee saved successfully.")
            return redirect('employee_list')
        return render(request, self.template_name, {'form': form})

def employee_create(request, pk=None):
    if pk:
        instance = get_object_or_404(Employee, pk=pk)
    else:
        instance = None

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            employee = form.save(commit=False)
            # Set the user field dynamically
            employee.user = f"{employee.first_name.lower()}.{employee.last_name.lower()}"
            employee.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=instance)

    return render(request, 'hr/employee_form.html', {'form': form})

# Employee Edit View
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)  # Retrieve the employee instance
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)  # Bind form with instance data
        if form.is_valid():
            form.save()  # Save the updated employee information
            return redirect('employee_list')  # Adjust to your redirect target
    else:
        form = EmployeeForm(instance=employee)  # Load existing employee data into the form

    return render(request, 'hr/employee_form.html', {'form': form, 'employee': employee})

# Employee Delete View
@require_POST
def employee_delete(request, pk):
    print(f"Attempting to delete employee with ID: {pk}")  # Log the ID of the employee being deleted
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    print(f"Employee {pk} deleted successfully.")
    return redirect('employee_list')

# Attendance List View
def attendance_list(request):
    attendance_records = Attendance.objects.all()
    return render(request, 'hr/attendance_list.html', {'attendance_records': attendance_records})

# Leave Tracker View
def leave_tracker(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'hr/leave_tracker.html', {'leave_requests': leave_requests})

# Attendance Report View
def attendance_report(request):
    return render(request, 'hr/attendance_report.html')

# Leave Request View
def leave_request(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Leave request submitted successfully.")
            return redirect('leave_success')
    else:
        form = LeaveForm()
    return render(request, 'hr/leave_request.html', {'form': form})

# Leave Report View
def leave_report(request):
    return render(request, 'hr/leave_report.html')

# Announcement List View
def announcement_list(request):
    announcements = Announcement.objects.all()
    return render(request, 'hr/announcement_list.html', {'announcements': announcements})

# Create Announcement View
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement created successfully.")
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'hr/create_announcement.html', {'form': form})

# Appraisal List View
def appraisal_list(request):
    appraisals = Appraisal.objects.all()
    return render(request, 'hr/appraisal_list.html', {'appraisals': appraisals})

# Create Appraisal View
def appraisal_create(request):
    if request.method == 'POST':
        form = AppraisalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appraisal_list')
    else:
        form = AppraisalForm()
    return render(request, 'hr/appraisal_form.html', {'form': form})

# Edit Appraisal View
def appraisal_edit(request, pk):
    appraisal = get_object_or_404(Appraisal, pk=pk)
    if request.method == 'POST':
        form = AppraisalForm(request.POST, instance=appraisal)
        if form.is_valid():
            form.save()
            return redirect('appraisal_list')
    else:
        form = AppraisalForm(instance=appraisal)
    return render(request, 'hr/appraisal_form.html', {'form': form})

# Delete Appraisal View
def appraisal_delete(request, pk):
    appraisal = get_object_or_404(Appraisal, pk=pk)
    if request.method == 'POST':
        appraisal.delete()
        return redirect('appraisal_list')
    return render(request, 'hr/appraisal_confirm_delete.html', {'appraisal': appraisal})

# Settings View
def settings_view(request):
    company_profile = CompanyProfile.objects.first()  
    departments = Department.objects.all()

    # Initialize forms before checking the POST request
    company_form = CompanyProfileForm(instance=company_profile)
    department_form = DepartmentForm()

    if request.method == 'POST':
        if 'update_company' in request.POST:
            company_form = CompanyProfileForm(request.POST, instance=company_profile)
            if company_form.is_valid():
                company_form.save()
                messages.success(request, "Company profile updated successfully.")
                return redirect('settings')

    context = {
        'company_form': company_form,
        'department_form': department_form,
        'departments': departments,
    }
    return render(request, 'hr/settings.html', context)


def edit_settings(request):
    # Retrieve the settings instance (assuming there's only one row in SiteSettings)
    site_settings = SiteSettings.objects.first()

    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=site_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect('edit_settings')
    else:
        form = SettingsForm(instance=site_settings)

    return render(request, 'hr/edit_settings.html', {'form': form})

def general_settings(request):
    # This is where you handle any logic related to general settings
    # You can query the database, process forms, etc.
    
    # Example: Sample context data (could be real settings data from the database)
    context = {
        'title': 'General Settings',
        'settings': {
            'site_name': 'My HR System',
            'timezone': 'Asia/Phnom_Penh',
            'language': 'English',
        }
    }

    # Render a template (assuming you have a template named 'general_settings.html')
    return render(request, 'hr/general_settings.html', context)

    # If you don’t have a template yet, you can simply return a basic response for now
    # return HttpResponse("General Settings Page")

def save_general_settings(request):
    if request.method == 'POST':
        setting1 = request.POST.get('setting1')
        setting2 = request.POST.get('setting2')

        # Get or create settings instance
        settings_instance, created = Settings.objects.get_or_create(id=1)  # Assuming a single instance
        settings_instance.setting1 = setting1
        settings_instance.setting2 = setting2
        settings_instance.save()

        messages.success(request, "General settings saved successfully!")
        return redirect('general_settings')
    
    return redirect('general_settings')

# Company Profile View
def company_profile(request):
    try:
        company = CompanyProfile.objects.first()
    except CompanyProfile.DoesNotExist:
        company = None
    return render(request, 'hr/company_profile.html', {'company': company})

# Edit Company Profile View
def edit_company_profile(request):
    pass  # Logic for editing the company profile

# Save Company Profile View
def save_company_profile(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        CompanyProfile.objects.update_or_create(
            defaults={'name': company_name, 'address': address}
        )
        messages.success(request, "Company profile saved successfully.")
        return redirect('settings')  
    return HttpResponse(status=405)

# Manage Departments View
def manage_departments(request):
    departments = Department.objects.all() 
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_departments')
    else:
        form = DepartmentForm()
    
    context = {
        'department_form': form,
        'departments': departments,
    }
    return render(request, 'hr/manage_departments.html', context)

# List Departments View
def list_departments(request):
    departments = Department.objects.all()
    return render(request, 'hr/list_departments.html', {'departments': departments})

# Add Department View
def add_department(request):
    if request.method == 'POST':
        department_form = DepartmentForm(request.POST)
        if department_form.is_valid():
            department_form.save()
            messages.success(request, "Department added successfully.")
            return redirect('list_departments')
    else:
        department_form = DepartmentForm()

    return render(request, 'hr/add_department.html', {'department_form': department_form})

# Delete Department View
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully.')
        return redirect('manage_departments')  # Redirect to your department management page

    return render(request, 'hr/confirm_delete.html', {'department': department}) 

# Resignation View
def resignation_view(request):
    resignations = Resignation.objects.all()
    return render(request, 'hr/resignation_list.html', {'resignations': resignations})

# Create Resignation View
def create_resignation(request):
    if request.method == 'POST':
        form = ResignationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Resignation submitted successfully.")
            return redirect('resignation_list')
    else:
        form = ResignationForm()
    return render(request, 'hr/create_resignation.html', {'form': form})

# Edit Resignation View
def edit_resignation(request, pk):
    resignation = get_object_or_404(Resignation, pk=pk)
    if request.method == 'POST':
        form = ResignationForm(request.POST, instance=resignation)
        if form.is_valid():
            form.save()
            messages.success(request, "Resignation updated successfully.")
            return redirect('resignation_list')
    else:
        form = ResignationForm(instance=resignation)
    return render(request, 'hr/edit_resignation.html', {'form': form})

# Delete Resignation View
def delete_resignation(request, pk):
    resignation = get_object_or_404(Resignation, pk=pk)
    if request.method == 'POST':
        resignation.delete()
        messages.success(request, 'Resignation deleted successfully.')
        return redirect('resignation_list')
    return render(request, 'hr/confirm_resignation_delete.html', {'resignation': resignation})

# Handle Resignation
def handle_resignation(request):
    # Placeholder function to handle resignation logic, such as notifying relevant parties
    # You can extend this as needed
    messages.info(request, "Resignation has been successfully processed.")
    return redirect('resignation_list')

# Announcement Detail View
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'hr/announcement_detail.html', {'announcement': announcement})

# Import for UserPermission (Custom permission checks)
from django.contrib.auth.mixins import LoginRequiredMixin

class RestrictedView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'hr/restricted.html')

# Custom Error Handling
def handle_404(request, exception):
    return render(request, '404.html', status=404)

def handle_500(request):
    return render(request, '500.html', status=500)