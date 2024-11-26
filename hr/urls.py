# hr/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import (
    employee_list,
    employee_detail,
    employee_create,
    employee_edit,
    employee_delete,
    attendance_report,
    leave_request,
    leave_report,
    announcement_list,
    create_announcement,
    ProfileView,
    EditProfileView,
    RecruitmentListView,
    settings_view,
    home,
    dashboard,
    manage_departments,
    list_departments,
    add_department,
    manage_departments, 
    delete_department,
    general_settings,
    save_general_settings,
    company_profile,
    save_company_profile,
    edit_settings,
    appraisal_list,
    appraisal_create,
    appraisal_edit,
    appraisal_delete,
    CompanyProfile,
)

urlpatterns = [
    # Home and Dashboard
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),

    # Employee Management
    path('employee-list/', employee_list, name='employee_list'),
    # path('employees/', employee_list, name='employee_list'),  # This line can be removed as it's a duplicate
    path('employees/<int:pk>/', employee_detail, name='employee_detail'),
    path('employees/create/', employee_create, name='employee_create'),
    path('employees/edit/<int:pk>/', employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', employee_delete, name='employee_delete'),

    # Attendance Management
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/report/', attendance_report, name='attendance_report'),

    # Leave Management
    path('leave-tracker/', views.leave_tracker, name='leave_tracker'),
    path('leave-request/', leave_request, name='leave_request'),
    path('leave-report/', leave_report, name='leave_report'),

    # Announcements
    path('announcements/', announcement_list, name='announcement_list'),
    path('announcements/create/', create_announcement, name='create_announcement'),

    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),

    # Recruitment
    path('recruitment/', RecruitmentListView.as_view(), name='recruitment_list'),

    # Company Profile Management
    # path('settings/company-profile/', views.CompanyProfile.as_view(), name='company_profile'),  # Make sure to change this to the appropriate view if needed
    path('settings/company-profile/', company_profile, name='company_profile'),
    path('company-profile/edit/', views.edit_company_profile, name='edit_company_profile'),

    # Department Management
    path('settings/manage-departments/', manage_departments, name='manage_departments'),
    path('departments/', list_departments, name='list_departments'),
    path('departments/add/', add_department, name='add_department'),
    path('settings/delete-department/', delete_department, name='delete_department'),

    # Settings Management
    path('settings/', settings_view, name='settings'),
    path('settings/general-settings/', general_settings, name='general_settings'),
    path('settings/save-general-settings/', save_general_settings, name='save_general_settings'),
    path('save-company-profile/', save_company_profile, name='save_company_profile'),
    path('settings/edit/', edit_settings, name='edit_settings'),

     # Appraisal Management
    path('appraisals/', appraisal_list, name='appraisal_list'),
    path('appraisals/create/', appraisal_create, name='appraisal_create'),
    path('appraisals/edit/<int:pk>/', appraisal_edit, name='appraisal_edit'),
    path('appraisals/<int:pk>/delete/', appraisal_delete, name='appraisal_delete'),
]

# Media file handling
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
