# hr/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Attendance, Leave, Appraisal, Announcement, Resignation
from .forms import LeaveForm, EmployeeForm, AnnouncementForm
from django.views import View
from django.views.generic import ListView
from .models import Recruitment
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import CompanyProfile, Department
from .forms import CompanyProfileForm, DepartmentForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Company  # Import your Company model if you have one

class RecruitmentListView(ListView):
    model = Recruitment
    template_name = 'hr/recruitment_list.html'  # Your template for listing recruitments

class ProfileView(View):
    def get(self, request):
        return render(request, 'hr/profile.html')  # Adjust the template path as needed
    
class EditProfileView(View):
    def get(self, request):
        employee = get_object_or_404(Employee, user=request.user)
        form = EmployeeForm(instance=employee)
        return render(request, 'hr/edit_profile.html', {'form': form})

    def post(self, request):
        employee = get_object_or_404(Employee, user=request.user)
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'hr/edit_profile.html', {'form': form})

def home(request):
    return render(request, 'hr/home.html')

def dashboard(request):
    total_employees = Employee.objects.count()
    total_leaves = Leave.objects.count()
    total_announcements = Announcement.objects.count()
    
    context = {
        'total_employees': total_employees,
        'total_leaves': total_leaves,
        'total_announcements': total_announcements,
    }
    return render(request, 'hr/dashboard.html', context)

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'hr/employee_list.html', {'employees': employees})

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'hr/employee_detail.html', {'employee': employee})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'hr/employee_form.html', {'form': form})

def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'hr/employee_form.html', {'form': form})

def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')  # Redirect to employee list after saving
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'hr/employee_form.html', {'form': form, 'employee': employee})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.delete()
        return redirect('employee_list')  # Redirect after deletion
    return render(request, 'hr/employee_confirm_delete.html', {'employee': employee})

def leave_request(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_success')  # Redirect after successful save
    else:
        form = LeaveForm()
    return render(request, 'hr/leave_request.html', {'form': form})

def announcement_list(request):
    announcements = Announcement.objects.all()
    return render(request, 'hr/announcement_list.html', {'announcements': announcements})

def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'hr/create_announcement.html', {'form': form})

class CompanyProfile(View):
    def get(self, request, *args, **kwargs):
        # Assuming you have a model called Company to fetch data
        company = Company.objects.first()  # Get the first company (modify as needed)
        context = {
            'company': company,  # Pass the company data to the template
        }
        return render(request, 'company_profile.html', context)

    def post(self, request, *args, **kwargs):
        # Handle form submission or other post logic here
        # Example: Updating company profile details
        # You can use request.POST to access submitted data
        return HttpResponse("Company profile updated!")  # Update this to suit your needs

def settings_view(request):
    company_profile = CompanyProfile.objects.first()  # Assuming there's only one profile
    departments = Department.objects.all()

    if request.method == 'POST':
        # Handle company profile update
        if 'update_company' in request.POST:
            company_form = CompanyProfileForm(request.POST, instance=company_profile)
            if company_form.is_valid():
                company_form.save()
                return redirect('settings')  # Redirect after saving

        # Handle department addition
        elif 'add_department' in request.POST:
            department_form = DepartmentForm(request.POST)
            if department_form.is_valid():
                department_form.save()
                return redirect('settings')  # Redirect after saving

    else:
        company_form = CompanyProfileForm(instance=company_profile)
        department_form = DepartmentForm()

    context = {
        'company_form': company_form,
        'department_form': department_form,
        'departments': departments,
    }
    return render(request, 'hr/settings.html', context)

def save_company_profile(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        # Save the company profile to the database
        CompanyProfile.objects.update_or_create(
            defaults={'name': company_name, 'address': address}
        )
        return redirect('settings')  # Redirect back to settings page after saving
    return HttpResponse(status=405)  # Method Not Allowed for non-POST requests

def manage_departments(request):
    # Your view logic here
    return render(request, 'your_template.html')

def add_department(request):
    if request.method == "POST":
        # Handle adding department logic here
        pass
    return render(request, 'hr/settings.html')
