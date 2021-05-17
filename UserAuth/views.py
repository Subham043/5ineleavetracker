from django.shortcuts import render, redirect
from django.contrib.auth import login as dj_login, authenticate, logout as dj_logout
from .forms import SignUpForm, ProfileForm
from employee.forms import PersonalForm, WorkForm, BankAccountForm, ExperienceForm, EducationForm
from department.forms import DepartmentForm
from designation.forms import DesignationForm
from roles.forms import RoleForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UserApproved, UserNotification
from employee.models import Personal, work, BankAccount, Experience, Education, PersonalImage
from department.models import department
from roles.models import roles
from leave.models import LeaveType, LeaveAvailable, ApplyLeave, HolidayList
from leave.forms import LeaveTypeForm, ApplyLeaveForm, HolidayListForm
from designation.models import designation
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from datetime import date


# Create your views here.



@login_required
def profile(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    try:
        user = User.objects.get(id=request.user.id)
        initial_dict_BankAccount = {
            "username" : user.username,
            "email" : user.email,
            "first_name" : user.first_name,
            "last_name" : user.last_name,
        }
        if request.method == 'POST':
            form = ProfileForm(request.POST, initial = initial_dict_BankAccount)
            if form.is_valid():
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()
                return render(request, 'profileupdate.html', {'form': form, 'success': 'Updated', 'userNotif': userNotif})
        else:
            form = ProfileForm(initial = initial_dict_BankAccount)
        return render(request, 'profileupdate.html', {'form': form, 'userNotif': userNotif})
    except:
        return redirect(adminDashboard)

@login_required
def passwordChange(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    try:
        user = User.objects.get(id=request.user.id)
        if request.method == 'POST':
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            repeat_new_password = request.POST.get("repeat_new_password")
            if user.check_password(old_password):
                if new_password == repeat_new_password:
                    user.set_password(new_password)
                    user.save()
                    dj_login(request, user)
                    return render(request, 'passwordchange.html', {'success': 'Updated', 'userNotif': userNotif})
                else:
                    return render(request, 'passwordchange.html', {'error': 'New Password and Repeated New Password does not match!!', 'userNotif': userNotif})
            else:
                return render(request, 'passwordchange.html', {'error': 'Please enter the correct Old Password', 'userNotif': userNotif})
        else:
            return render(request, 'passwordchange.html', {'userNotif': userNotif})
    except:
        return redirect(adminDashboard)



@login_required
def bankPage(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False

    try:
        BankAccountEmployee = BankAccount.objects.get(Employee=request.user)
        initial_dict_BankAccount = {
            "Bank_Name" : BankAccountEmployee.Bank_Name,
            "Account_Number" : BankAccountEmployee.Account_Number,
            "Branch_Name" : BankAccountEmployee.Branch_Name,
            "IFSC_Code" : BankAccountEmployee.IFSC_Code,
        }
        if request.method == 'POST':
            BankAccountform = BankAccountForm(request.POST, initial = initial_dict_BankAccount)
            if BankAccountform.is_valid():
                BankAccountEmployee.Bank_Name = request.POST.get("Bank_Name")
                BankAccountEmployee.Account_Number = request.POST.get("Account_Number")
                BankAccountEmployee.Branch_Name = request.POST.get("Branch_Name")
                BankAccountEmployee.IFSC_Code = request.POST.get("IFSC_Code")
                BankAccountEmployee.save()
                return render(request, 'bank.html', { 'BankAccountform':BankAccountform, 'success': True, 'successMessage': 'Bank Account Updated Successfully', 'userNotif': userNotif})
        else:
            BankAccountform = BankAccountForm(initial = initial_dict_BankAccount)
    except:
        initial_dict_BankAccount = {}
        if request.method == 'POST':
            BankAccountform = BankAccountForm(request.POST, initial = initial_dict_BankAccount)
            if BankAccountform.is_valid():
                Bank_Name = request.POST.get("Bank_Name")
                Account_Number = request.POST.get("Account_Number")
                Branch_Name = request.POST.get("Branch_Name")
                IFSC_Code = request.POST.get("IFSC_Code")
                Employee = request.user
                user = BankAccount.objects.create(Bank_Name=Bank_Name,Account_Number=Account_Number, Branch_Name=Branch_Name, IFSC_Code=IFSC_Code, Employee=Employee)
                return render(request, 'bank.html', {'BankAccountform':BankAccountform,'success': True, 'successMessage': 'Bank Account Updated Successfully', 'userNotif': userNotif})
        else:
            BankAccountform = BankAccountForm(initial = initial_dict_BankAccount)
    # return render(request, 'profile.html', {'form': form, 'workForm': workForm, 'BankAccountform':BankAccountform, 'Experienceform':Experienceform, 'Educationform':Educationform})
    return render(request, 'bank.html', {'BankAccountform':BankAccountform, 'userNotif': userNotif})

@login_required
def educationPage(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    try:
        EducationEmployee = Education.objects.get(Employee=request.user)
        initial_dict_Education = {
            "School_Name" : EducationEmployee.School_Name,
            "Degree_Or_Diploma" : EducationEmployee.Degree_Or_Diploma,
            "Field_Of_Study" : EducationEmployee.Field_Of_Study,
            "Date_Of_Completion" : EducationEmployee.Date_Of_Completion,
            "Interests" : EducationEmployee.Interests,
        }
        if request.method == 'POST':
            Educationform = EducationForm(request.POST, initial = initial_dict_Education)
            if Educationform.is_valid():
                EducationEmployee.School_Name = request.POST.get("School_Name")
                EducationEmployee.Degree_Or_Diploma = request.POST.get("Degree_Or_Diploma")
                EducationEmployee.Field_Of_Study = request.POST.get("Field_Of_Study")
                EducationEmployee.Date_Of_Completion = request.POST.get("Date_Of_Completion")
                EducationEmployee.Interests = request.POST.get("Interests")
                EducationEmployee.save()
                return render(request, 'education.html', {'Educationform':Educationform, 'success': True, 'successMessage': 'Education Profile Updated Successfully', 'userNotif': userNotif})
        else:
            Educationform = EducationForm(initial = initial_dict_Education)
    except:
        initial_dict_Education = {}
        if request.method == 'POST':
            Educationform = EducationForm(request.POST, initial = initial_dict_Education)
            if Educationform.is_valid():
                School_Name = request.POST.get("School_Name")
                Degree_Or_Diploma = request.POST.get("Degree_Or_Diploma")
                Field_Of_Study = request.POST.get("Field_Of_Study")
                Date_Of_Completion = request.POST.get("Date_Of_Completion")
                Interests = request.POST.get("Interests")
                Employee = request.user
                user = Education.objects.create(School_Name=School_Name,Degree_Or_Diploma=Degree_Or_Diploma, Field_Of_Study=Field_Of_Study, Date_Of_Completion=Date_Of_Completion, Interests=Interests, Employee=Employee)
                return render(request, 'education.html', {'Educationform':Educationform, 'success': True, 'successMessage': 'Education Profile Updated Successfully', 'userNotif': userNotif})
        else:
            Educationform = EducationForm(initial = initial_dict_Education)

    # return render(request, 'profile.html', {'form': form, 'workForm': workForm, 'BankAccountform':BankAccountform, 'Experienceform':Experienceform, 'Educationform':Educationform})
    return render(request, 'education.html', {'Educationform':Educationform, 'userNotif': userNotif})


@login_required
def experiencePage(request):

    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False

    try:
        ExperienceEmployee = Experience.objects.get(Employee=request.user)
        initial_dict_Experience = {
            "Previous_Company_Name" : ExperienceEmployee.Previous_Company_Name,
            "Job_Title" : ExperienceEmployee.Job_Title,
            "From" : ExperienceEmployee.From,
            "To" : ExperienceEmployee.To,
            "Job_Description" : ExperienceEmployee.Job_Description,
        }
        if request.method == 'POST':
            Experienceform = ExperienceForm(request.POST, initial = initial_dict_Experience)
            if Experienceform.is_valid():
                ExperienceEmployee.Previous_Company_Name = request.POST.get("Previous_Company_Name")
                ExperienceEmployee.Job_Title = request.POST.get("Job_Title")
                ExperienceEmployee.From = request.POST.get("From")
                ExperienceEmployee.To = request.POST.get("To")
                ExperienceEmployee.Job_Description = request.POST.get("Job_Description")
                ExperienceEmployee.save()
                return render(request, 'experience.html', {'Experienceform':Experienceform, 'success': True, 'successMessage': 'Experience Profile Updated Successfully', 'userNotif': userNotif})
        else:
            Experienceform = ExperienceForm(initial = initial_dict_Experience)
    except:
        initial_dict_Experience = {}
        if request.method == 'POST':
            Experienceform = ExperienceForm(request.POST, initial = initial_dict_Experience)
            if Experienceform.is_valid():
                Previous_Company_Name = request.POST.get("Previous_Company_Name")
                Job_Title = request.POST.get("Job_Title")
                From = request.POST.get("From")
                To = request.POST.get("To")
                Job_Description = request.POST.get("Job_Description")
                Employee = request.user
                user = Experience.objects.create(Previous_Company_Name=Previous_Company_Name,Job_Title=Job_Title, From=From, To=To, Job_Description=Job_Description, Employee=Employee)
                return render(request, 'experience.html', {'Experienceform':Experienceform, 'success': True, 'successMessage': 'Experience Profile Updated Successfully', 'userNotif': userNotif})
        else:
            Experienceform = ExperienceForm(initial = initial_dict_Experience)

    # return render(request, 'profile.html', {'form': form, 'workForm': workForm, 'BankAccountform':BankAccountform, 'Experienceform':Experienceform, 'Educationform':Educationform})
    return render(request, 'experience.html', {'Experienceform':Experienceform, 'userNotif': userNotif})


@login_required
def workPage(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False

    try:
        workEmployee = work.objects.get(Employee=request.user)
        print(workEmployee)
        initial_dict_work = {
            "Department" : workEmployee.Department,
            "Reporting_To" : workEmployee.Reporting_To,
            "Source_Of_Hire" : workEmployee.Source_Of_Hire,
            "Location" : workEmployee.Location,
            "Title" : workEmployee.Title,
            "Date_Of_Joining" : workEmployee.Date_Of_Joining,
            "Employee_Status" : workEmployee.Employee_Status,
            "Employee_Type" : workEmployee.Employee_Type,
            "Work_Phone" : workEmployee.Work_Phone,
            "Extension" : workEmployee.Extension,
            "Role" : workEmployee.Role,
        }
        if request.method == 'POST':
            workForm = WorkForm(request.POST, initial = initial_dict_work)
            if workForm.is_valid():
                DepartmentLead = request.POST.get("Department")
                workEmployee.Department = department.objects.get(id=DepartmentLead)
                ReportingTo = request.POST.get("Reporting_To")
                workEmployee.Reporting_To = User.objects.get(id=ReportingTo)
                SourceOfHire = request.POST.get("Source_Of_Hire")
                workEmployee.Source_Of_Hire = User.objects.get(id=SourceOfHire)
                workEmployee.Location = request.POST.get("Location")
                Designation = request.POST.get("Title")
                workEmployee.Title = designation.objects.get(id=Designation)
                workEmployee.Date_Of_Joining = request.POST.get("Date_Of_Joining")
                workEmployee.Employee_Status = request.POST.get("Employee_Status")
                workEmployee.Employee_Type = request.POST.get("Employee_Type")
                workEmployee.Work_Phone = request.POST.get("Work_Phone")
                workEmployee.Extension = request.POST.get("Extension")
                Roles = request.POST.get("Role")
                workEmployee.Role = roles.objects.get(id=Roles)
                workEmployee.save()
                return render(request, 'work.html', {'workForm': workForm, 'success': True, 'successMessage': 'Work Profile Updated Successfully', 'userNotif': userNotif})
        else:
            workForm = WorkForm(initial = initial_dict_work)
    except:
        initial_dict_work = {}
        if request.method == 'POST':
            workForm = WorkForm(request.POST, initial = initial_dict_work)
            if workForm.is_valid():
                Department = request.POST.get("Department")
                DepartmentLead = department.objects.get(id=Department)
                Reporting_To = request.POST.get("Reporting_To")
                ReportingTo = User.objects.get(id=Reporting_To)
                Source_Of_Hire = request.POST.get("Source_Of_Hire")
                SourceOfHire = User.objects.get(id=Source_Of_Hire)
                Location = request.POST.get("Location")
                Title = request.POST.get("Title")
                Designation = designation.objects.get(id=Title)
                Date_Of_Joining = request.POST.get("Date_Of_Joining")
                Employee_Status = request.POST.get("Employee_Status")
                Employee_Type = request.POST.get("Employee_Type")
                Work_Phone = request.POST.get("Work_Phone")
                Extension = request.POST.get("Extension")
                Role = request.POST.get("Role")
                Roles = roles.objects.get(id=Role)
                Employee = request.user
                user = work.objects.create(Department=DepartmentLead,Reporting_To=ReportingTo,Source_Of_Hire=SourceOfHire,Location=Location,Title=Designation,Date_Of_Joining=Date_Of_Joining,Employee_Status=Employee_Status,Employee_Type=Employee_Type,Work_Phone=Work_Phone,Extension=Extension,Role=Roles,Employee=Employee)
                return render(request, 'work.html', {'workForm': workForm, 'success': True, 'successMessage': 'Work Profile Updated Successfully', 'userNotif': userNotif})
        else:
            workForm = WorkForm(initial = initial_dict_work)

    # return render(request, 'profile.html', {'form': form, 'workForm': workForm, 'BankAccountform':BankAccountform, 'Experienceform':Experienceform, 'Educationform':Educationform})
    return render(request, 'work.html', {'workForm': workForm, 'userNotif': userNotif})


@login_required
def personal(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    profileimage = PersonalImage.objects.get(Employee=request.user)
    try:
        
        employee = Personal.objects.get(Employee=request.user)
        initial_dict_personal = {
            "Mobile_Phone" : employee.Mobile_Phone,
            "Other_Email" : employee.Other_Email,
            "Address" : employee.Address,
            "Date_Of_Birth" : employee.Date_Of_Birth,
            "MARITAL_STATUS" : employee.MARITAL_STATUS,
            "Gender" : employee.Gender,
        }
        if request.POST.get('updateFormValues'):
            form = PersonalForm(request.POST or None, initial = initial_dict_personal)
            if form.is_valid():
                employee.Mobile_Phone = request.POST.get("Mobile_Phone")
                employee.Other_Email = request.POST.get("Other_Email")
                employee.Address = request.POST.get("Address")
                employee.Date_Of_Birth = request.POST.get("Date_Of_Birth")
                employee.MARITAL_STATUS = request.POST.get("MARITAL_STATUS")
                employee.Gender = request.POST.get("Gender")
                employee.save()
                return render(request, 'personal.html', {'form': form, 'success': True, 'successMessage': 'Personal Profile Updated Successfully', 'profileimage': profileimage, 'userNotif': userNotif})

        elif request.POST.get('imageUpdateBtn'):
            form = PersonalForm(initial = initial_dict_personal)
            try:
                images = request.FILES["image"]
                print(images)
                profileimage.image.delete()
                profileimage.image = images
                profileimage.save()
                return render(request, 'personal.html', {'form': form, 'success': True, 'successMessage': 'Profile Image Updated Successfully', 'profileimage': profileimage,'userNotif': userNotif})
            except:
                return render(request, 'personal.html', {'form': form, 'profileimage': profileimage, 'userNotif': userNotif})

        else:
            form = PersonalForm(initial = initial_dict_personal)

    except:
        
        initial_dict_personal = {
            "Mobile_Phone" : "",
            "Other_Email" : "",
            "Address" : "",
        }
        if request.POST.get('updateFormValues'):
            form = PersonalForm(request.POST, initial = initial_dict_personal)
            if form.is_valid():
                Mobile_Phone = request.POST.get("Mobile_Phone")
                Other_Email = request.POST.get("Other_Email")
                Address = request.POST.get("Address")
                Date_Of_Birth = request.POST.get("Date_Of_Birth")
                MARITAL_STATUS = request.POST.get("MARITAL_STATUS")
                Gender = request.POST.get("Gender")
                Employee = request.user
                user = Personal.objects.create(Mobile_Phone=Mobile_Phone,Other_Email=Other_Email, Address=Address, Date_Of_Birth=Date_Of_Birth, MARITAL_STATUS=MARITAL_STATUS, Gender=Gender, Employee=Employee)
                return render(request, 'personal.html', {'form': form, 'success': True, 'successMessage': 'Personal Profile Updated Successfully', 'userNotif': userNotif})
        
        elif request.POST.get('imageUpdateBtn'):
            form = PersonalForm(initial = initial_dict_personal)
            try:
                images = request.FILES["image"]
                print(images)
                profileimage.image.delete()
                profileimage.image = images
                profileimage.save()
                return render(request, 'personal.html', {'form': form, 'success': True, 'successMessage': 'Profile Image Updated Successfully', 'profileimage': profileimage, 'userNotif': userNotif})
            except:
                return render(request, 'personal.html', {'form': form, 'profileimage': profileimage, 'userNotif': userNotif})

        else:
            form = PersonalForm(initial = initial_dict_personal)
    # return render(request, 'profile.html', {'form': form, 'workForm': workForm, 'BankAccountform':BankAccountform, 'Experienceform':Experienceform, 'Educationform':Educationform})
    return render(request, 'personal.html', {'form': form, 'profileimage': profileimage, 'userNotif': userNotif})

@login_required
def EmployeeTable(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    employees = UserApproved.objects.filter(AdminApproved=True)
    return render(request, 'employeeTable.html', {'employees':employees, 'userNotif': userNotif})

@login_required
def LeaveAppliedTable(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
        userNotif.LeaveStatus = False
        userNotif.save()
    except:
        userNotif = False
    employees = ApplyLeave.objects.filter(Employee=request.user).order_by('-timestamp')
    return render(request, 'leaveappliedTable.html', {'employees':employees, 'userNotif': userNotif})

@login_required
def ApproveEmployeeLeaveTable(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
        userNotif.NewLeave = False
        userNotif.save()
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    if request.method == 'POST':
        id_user = request.POST.get("id_user")
        reason = request.POST.get("reason")
        if reason == '':
            reason = "Not Specified"
        try:
            userApproved = ApplyLeave.objects.get(id=id_user)
            userApproved.Rejected = True
            userApproved.Reason_For_Rejection = reason
            userApproved.save()
            userNotify = UserNotification.objects.get(Employee=userApproved.Employee.id)
            print(userNotify)
            userNotify.LeaveStatus = True
            userNotify.save()
            availableleave = LeaveAvailable.objects.get(employee=userApproved.Employee, leavetype=userApproved.Leave_Type)
            if userApproved.Leave_Type.Unit == "DY":
                print(int(availableleave.leaveBooked) - 1)
                availableleave.leaveBooked = int(availableleave.leaveBooked) - 1
                availableleave.save()
            else:
                availableleave.leaveBooked = int(availableleave.leaveBooked) - 0.5
                availableleave.save()

        except:
            pass
        return redirect(ApproveEmployeeLeaveSuccess, success="Rejected")
    else:
        employees = ApplyLeave.objects.filter(Approved=False,Rejected=False)
        return render(request, 'approveemployeeleaveTable.html', {'employees':employees, 'userNotif': userNotif})


@login_required
def ApproveEmployeeLeaveSuccess(request,success):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
        userNotif.NewLeave = False
        userNotif.save()
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    if request.method == 'POST':
        id_user = request.POST.get("id_user")
        reason = request.POST.get("reason")
        if reason == '':
            reason = "Not Specified"
        try:
            userApproved = ApplyLeave.objects.get(id=id_user)
            userApproved.Rejected = True
            userApproved.Reason_For_Rejection = reason
            userApproved.save()
            userNotify = UserNotification.objects.get(Employee=userApproved.Employee.id)
            userNotify.LeaveStatus = True
            userNotify.save()
            availableleave = LeaveAvailable.objects.get(employee=userApproved.Employee, leavetype=userApproved.Leave_Type)
            if userApproved.Leave_Type.Unit == "DY":
                print(int(availableleave.leaveBooked) - 1)
                availableleave.leaveBooked = int(availableleave.leaveBooked) - 1
                availableleave.save()
            else:
                availableleave.leaveBooked = int(availableleave.leaveBooked) - 0.5
                availableleave.save()

        except:
            pass
        return redirect(ApproveEmployeeLeaveSuccess, success="Rejected")
    else:
        employees = ApplyLeave.objects.filter(Approved=False,Rejected=False)
        return render(request, 'approveemployeeleaveTable.html', {'employees':employees, 'success':success, 'userNotif': userNotif})


@login_required
def approveLeave(request,id):
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    try:
        userApproved = ApplyLeave.objects.get(id=id)
        LeaveBooked = LeaveAvailable.objects.get(employee=userApproved.Employee.id, leavetype=userApproved.Leave_Type)
        userNotify = UserNotification.objects.get(Employee=userApproved.Employee.id)
        if LeaveBooked.leaveAvailable >= LeaveBooked.leaveBooked:
            userApproved.Approved = True
            userApproved.save()
            userNotify.LeaveStatus = True
            userNotify.save()
            if LeaveBooked.leavetype.Unit == 'DY':
                LeaveBooked.leaveBooked = int(LeaveBooked.leaveBooked)+1
                LeaveBooked.save()
            else:
                LeaveBooked.leaveBooked = int(LeaveBooked.leaveBooked)+0.5
                LeaveBooked.save()
    except:
        pass
    return redirect(ApproveEmployeeLeaveSuccess, success="Approved")


@login_required
def ApproveEmployeeTable(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
        userNotif.NewEmployee = False
        userNotif.save()
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    employees = UserApproved.objects.filter(AdminApproved=False)
    return render(request, 'approveemployeeTable.html', {'employees':employees, 'userNotif': userNotif})

@login_required
def ApproveEmployeeSuccess(request,success):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
        userNotif.NewEmployee = False
        userNotif.save()
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    employees = UserApproved.objects.filter(AdminApproved=False)
    return render(request, 'approveemployeeTable.html', {'employees':employees, 'success':success, 'userNotif': userNotif})

@login_required
def EmployeeDetailTable(request, pk):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    try:
        personalDetail = Personal.objects.get(Employee=pk)
    except:
        personalDetail = {'empty':True}
    try:
        workDetail = work.objects.get(Employee=pk)
    except:
        workDetail = {'empty':True}
    try:
        experienceDetail = Experience.objects.get(Employee=pk)
    except:
        experienceDetail = {'empty':True}
    try:
        educationDetail = Education.objects.get(Employee=pk)
    except:
        educationDetail = {'empty':True}
    return render(request, 'employeedetailTable.html', {'personalDetail':personalDetail, 'workDetail':workDetail, 'experienceDetail':experienceDetail, 'educationDetail':educationDetail, 'userNotif': userNotif})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = form.save()
            c = UserApproved(Employee = user)
            c.save()
            c = UserNotification(Employee = user)
            c.save()
            return redirect(login)
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

@login_required
def logout(request):
    dj_logout(request)
    return redirect(login)

@login_required
def HolidayListTable(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    depTable = HolidayList.objects.all()
    return render(request, 'HolidayListTable.html', {'depTable':depTable, 'userNotif': userNotif})


@login_required
def AddHolidayList(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    if request.method == 'POST':
        departmentForm = HolidayListForm(request.POST)
        if departmentForm.is_valid():
            Name = request.POST.get("Name")
            Date = request.POST.get("Date")
            Type = request.POST.get("Type")
            EveryYear = request.POST.get("EveryYear")
            if EveryYear == 'on':
                EveryYear = True
            else:
                EveryYear = False
            Description = request.POST.get("Description")
            user = HolidayList.objects.create(Name=Name, Date=Date, Type=Type, EveryYear=EveryYear, Description=Description)
        # return render(request, 'department.html', {'departmentForm':departmentForm, 'success': True})
            return redirect(AddHolidayListSuccess, success="Added")
    else:
        departmentForm = HolidayListForm()
    return render(request, 'holidaylist.html', {'departmentForm':departmentForm, 'userNotif': userNotif})


@login_required
def EditHolidayList(request,pk):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    try:
        departmentValue = HolidayList.objects.get(id=pk)
        initial_dict_department = {
            "Name" : departmentValue.Name,
            "Date" : departmentValue.Date,
            "Type" : departmentValue.Type,
            "EveryYear" : departmentValue.EveryYear,
            "Description" : departmentValue.Description,
        }
    except:
        initial_dict_department = {}
    if request.method == 'POST':
        departmentForm = HolidayListForm(request.POST, initial = initial_dict_department)
        if departmentForm.is_valid():
            departmentValue.Name = request.POST.get("Name")
            departmentValue.Date = request.POST.get("Date")
            departmentValue.Type = request.POST.get("Type")
            EveryYear = request.POST.get("EveryYear")
            if EveryYear == 'on':
                departmentValue.EveryYear = True
            else:
                departmentValue.EveryYear = False
            departmentValue.Description = request.POST.get("Description")
            departmentValue.save()
            return redirect(AddHolidayListSuccess, success="Updated")
    else:
        departmentForm = HolidayListForm(initial = initial_dict_department)
    return render(request, 'holidaylistEdit.html', {'departmentForm':departmentForm, 'userNotif': userNotif})


@login_required
def DeleteHolidayList(request,pk):
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    try:
        depTable = HolidayList.objects.get(id=pk)
    except:
        pass
    depTable.delete()
    return redirect(AddHolidayListSuccess, success="Deleted")

@login_required
def AddHolidayListSuccess(request,success):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    depTable = HolidayList.objects.all()
    return render(request, 'HolidayListTable.html', {'depTable':depTable, 'success':success, 'userNotif': userNotif})

@login_required
def LeaveTypeTable(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    depTable = LeaveType.objects.all()
    return render(request, 'leavetypeTable.html', {'depTable':depTable, 'userNotif': userNotif})

@login_required
def AddLeaveTypeSuccess(request,success):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    depTable = LeaveType.objects.all()
    return render(request, 'leavetypeTable.html', {'depTable':depTable, 'success':success, 'userNotif': userNotif})


@login_required
def DeleteLeaveType(request,pk):
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    try:
        depTable = LeaveType.objects.get(id=pk)
    except:
        pass
    depTable.delete()
    return redirect(AddLeaveTypeSuccess, success="Deleted")


@login_required
def AddLeaveType(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    if request.method == 'POST':
        departmentForm = LeaveTypeForm(request.POST)
        if departmentForm.is_valid():
            Name = request.POST.get("Name")
            Code = request.POST.get("Code")
            Leave_Type = request.POST.get("Leave_Type")
            Unit = request.POST.get("Unit")
            Description = request.POST.get("Description")
            Valid_From = request.POST.get("Valid_From")
            Valid_To = request.POST.get("Valid_To")
            Opening_Balance = request.POST.get("Opening_Balance")
            Maximum_Balance = request.POST.get("Maximum_Balance")
            Holiday_Between_Leave_Period = request.POST.get("Holiday_Between_Leave_Period")
            To_Be_Applied_Days_In_Advance = request.POST.get("To_Be_Applied_Days_In_Advance")
            Maximum_Number_Of_Consecutive_Days_Of_Leave_Allowed = request.POST.get("Maximum_Number_Of_Consecutive_Days_Of_Leave_Allowed")
            Minimum_Gap_Between_2_Application_In_Days = request.POST.get("Minimum_Gap_Between_2_Application_In_Days")
            user = LeaveType.objects.create(Name=Name, Code=Code, Leave_Type=Leave_Type, Unit=Unit, Description=Description, Valid_From=Valid_From, Valid_To=Valid_To, Opening_Balance=Opening_Balance, Maximum_Balance=Maximum_Balance, Holiday_Between_Leave_Period=Holiday_Between_Leave_Period, To_Be_Applied_Days_In_Advance=To_Be_Applied_Days_In_Advance, Maximum_Number_Of_Consecutive_Days_Of_Leave_Allowed=Maximum_Number_Of_Consecutive_Days_Of_Leave_Allowed, Minimum_Gap_Between_2_Application_In_Days=Minimum_Gap_Between_2_Application_In_Days)
        # return render(request, 'department.html', {'departmentForm':departmentForm, 'success': True})
            return redirect(AddLeaveTypeSuccess, success="Added")
    else:
        departmentForm = LeaveTypeForm()
    return render(request, 'leavetype.html', {'departmentForm':departmentForm, 'userNotif': userNotif})

@login_required
def EditLeaveType(request,pk):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    try:
        departmentValue = LeaveType.objects.get(id=pk)
        initial_dict_department = {
            "Name" : departmentValue.Name,
            "Code" : departmentValue.Code,
            "Leave_Type" : departmentValue.Leave_Type,
            "Unit" : departmentValue.Unit,
            "Description" : departmentValue.Description,
            "Valid_From" : departmentValue.Valid_From,
            "Valid_To" : departmentValue.Valid_To,
            "Opening_Balance" : departmentValue.Opening_Balance,
            "Maximum_Balance" : departmentValue.Maximum_Balance,
            "Holiday_Between_Leave_Period" : departmentValue.Holiday_Between_Leave_Period,
            "Maximum_Number_Of_Consecutive_Days_Of_Leave_Allowed" : departmentValue.Maximum_Number_Of_Consecutive_Days_Of_Leave_Allowed,
            "Minimum_Gap_Between_2_Application_In_Days" : departmentValue.Minimum_Gap_Between_2_Application_In_Days,
            "To_Be_Applied_Days_In_Advance" : departmentValue.To_Be_Applied_Days_In_Advance,
        }
    except:
        initial_dict_department = {}
    if request.method == 'POST':
        departmentForm = LeaveTypeForm(request.POST, initial = initial_dict_department)
        if departmentForm.is_valid():
            departmentValue.Name = request.POST.get("Name")
            departmentValue.Code = request.POST.get("Code")
            departmentValue.Leave_Type = request.POST.get("Leave_Type")
            departmentValue.Unit = request.POST.get("Unit")
            departmentValue.Description = request.POST.get("Description")
            departmentValue.Valid_From = request.POST.get("Valid_From")
            departmentValue.Valid_To = request.POST.get("Valid_To")
            departmentValue.Opening_Balance = request.POST.get("Opening_Balance")
            departmentValue.Maximum_Balance = request.POST.get("Maximum_Balance")
            departmentValue.Holiday_Between_Leave_Period = request.POST.get("Holiday_Between_Leave_Period")
            departmentValue.To_Be_Applied_Days_In_Advance = request.POST.get("To_Be_Applied_Days_In_Advance")
            departmentValue.Maximum_Number_Of_Consecutive_Days_Of_Leave_Allowed = request.POST.get("Maximum_Number_Of_Consecutive_Days_Of_Leave_Allowed")
            departmentValue.Minimum_Gap_Between_2_Application_In_Days = request.POST.get("Minimum_Gap_Between_2_Application_In_Days")
            departmentValue.save()
            return redirect(AddLeaveTypeSuccess, success="Updated")
    else:
        departmentForm = LeaveTypeForm(initial = initial_dict_department)
    return render(request, 'leavetypeEdit.html', {'departmentForm':departmentForm, 'userNotify': userNotif})

@login_required
def LeaveManagerTable(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    leaveAvailable = LeaveAvailable.objects.filter(employee=request.user)
    holidayList = HolidayList.objects.all()
    birthdaylist = Personal.objects.all()
    return render(request, 'leavemanagertable.html', {'leaveAvailable':leaveAvailable, 'holidayList':holidayList, 'birthdaylist':birthdaylist, 'userNotif': userNotif})

@login_required
def ApplyLeavePage(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.method == 'POST':
        form = ApplyLeaveForm(request.POST)
        if form.is_valid():
            Leave_Type = request.POST.get("Leave_Type")
            leaveType = LeaveType.objects.get(id=Leave_Type)
            Valid_From = request.POST.get("Valid_From")
            Valid_To = request.POST.get("Valid_To")
            Team_Email_ID = request.POST.get("Team_Email_ID")
            Reason_For_Leave = request.POST.get("Reason_For_Leave")
            Employee = request.user
            availableleave = LeaveAvailable.objects.get(employee=request.user, leavetype=leaveType)
            if availableleave.leaveBooked < availableleave.leaveAvailable:
                if leaveType.Unit == "DY":
                    availableleave.leaveBooked = int(availableleave.leaveBooked) + 1
                    availableleave.save()
                else:
                    availableleave.leaveBooked = int(availableleave.leaveBooked) + 0.5
                    availableleave.save()
            else:
                return render(request, 'applyleaveform.html', {'form':form, 'error':'Sorry, You have no '+ str(availableleave.leavetype) + ' available', 'userNotif': userNotif})
            try:
                lastLeaveApplied = ApplyLeave.objects.filter(Employee=request.user).last()
                lastLeave = date(lastLeaveApplied.timestamp.year, lastLeaveApplied.timestamp.month, lastLeaveApplied.timestamp.day)
                today = datetime.today()
                currentLeave = date(today.year, today.month, today.day)
                diff = currentLeave - lastLeave
                leaveAvail = LeaveType.objects.get(id=leaveType.id)
                count = int(leaveAvail.Minimum_Gap_Between_2_Application_In_Days) - int(diff.days)
                if int(diff.days) < int(leaveAvail.Minimum_Gap_Between_2_Application_In_Days):
                    return render(request, 'applyleaveform.html', {'form':form, 'error':'Sorry, You recently applied for '+ str(lastLeaveApplied.Leave_Type) + ' ' + str(diff.days) + ' days back. You need to wait for ' + str(count) + ' days in order to apply again', 'userNotif': userNotif})
            except:
                pass 
            user = ApplyLeave.objects.create(Leave_Type=leaveType, Valid_From=Valid_From, Valid_To=Valid_To, Team_Email_ID=Team_Email_ID, Reason_For_Leave=Reason_For_Leave, Employee=Employee)
        # return render(request, 'department.html', {'departmentForm':departmentForm, 'success': True})
            return render(request, 'applyleaveform.html', {'form':form, 'success':'Leave Applied Successfully', 'userNotif': userNotif})
    else:
        form = ApplyLeaveForm()
    return render(request, 'applyleaveform.html', {'form':form, 'userNotif': userNotif})

@login_required
def RoleTable(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    depTable = roles.objects.all()
    return render(request, 'roleTable.html', {'depTable':depTable, 'userNotif': userNotif})

@login_required
def AddRoleSuccess(request,success):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    depTable = roles.objects.all()
    return render(request, 'roleTable.html', {'depTable':depTable, 'success':success, 'userNotif': userNotif})

@login_required
def DeleteRole(request,pk):
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    try:
        depTable = roles.objects.get(id=pk)
    except:
        pass
    depTable.delete()
    return redirect(AddRoleSuccess, success="Deleted")

@login_required
def AddRole(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    if request.method == 'POST':
        departmentForm = RoleForm(request.POST)
        if departmentForm.is_valid():
            Role_Name = request.POST.get("Role_Name")
            user = roles.objects.create(Role_Name=Role_Name)
        # return render(request, 'department.html', {'departmentForm':departmentForm, 'success': True})
            return redirect(AddRoleSuccess, success="Added")
    else:
        departmentForm = RoleForm()
    return render(request, 'role.html', {'departmentForm':departmentForm, 'userNotif': userNotif})

@login_required
def EditRole(request,pk):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    try:
        departmentValue = roles.objects.get(id=pk)
        initial_dict_department = {
            "Role_Name" : departmentValue.Role_Name,
        }
    except:
        initial_dict_department = {}
    if request.method == 'POST':
        departmentForm = RoleForm(request.POST, initial = initial_dict_department)
        if departmentForm.is_valid():
            departmentValue.Role_Name = request.POST.get("Role_Name")
            departmentValue.save()
        return redirect(AddRoleSuccess, success="Updated")
    else:
        departmentForm = RoleForm(initial = initial_dict_department)
    return render(request, 'roleEdit.html', {'departmentForm':departmentForm, 'userNotif': userNotif})

@login_required
def DesignationTable(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    depTable = designation.objects.all()
    return render(request, 'designationTable.html', {'depTable':depTable, 'userNotif': userNotif})
    

@login_required
def AddDesignation(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    if request.method == 'POST':
        departmentForm = DesignationForm(request.POST)
        if departmentForm.is_valid():
            Designation_Name = request.POST.get("Designation_Name")
            Stream = request.POST.get("Stream")
            Mail_Alias = request.POST.get("Mail_Alias")
            user = designation.objects.create(Designation_Name=Designation_Name,Stream=Stream, Mail_Alias=Mail_Alias)
        # return render(request, 'department.html', {'departmentForm':departmentForm, 'success': True})
            return redirect(AddDesignationSuccess, success="Added")
    else:
        departmentForm = DesignationForm()
    return render(request, 'designation.html', {'departmentForm':departmentForm, 'userNotif': userNotif})

@login_required
def EditDesignation(request,pk):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    try:
        departmentValue = designation.objects.get(id=pk)
        initial_dict_department = {
            "Designation_Name" : departmentValue.Designation_Name,
            "Stream" : departmentValue.Stream,
            "Mail_Alias" : departmentValue.Mail_Alias,
        }
    except:
        initial_dict_department = {}
    if request.method == 'POST':
        departmentForm = DesignationForm(request.POST, initial = initial_dict_department)
        if departmentForm.is_valid():
            departmentValue.Designation_Name = request.POST.get("Designation_Name")
            departmentValue.Stream = request.POST.get("Stream")
            departmentValue.Mail_Alias = request.POST.get("Mail_Alias")
            departmentValue.save()
        return redirect(AddDesignationSuccess, success="Updated")
    else:
        departmentForm = DesignationForm(initial = initial_dict_department)
    return render(request, 'designationEdit.html', {'departmentForm':departmentForm, 'userNotif': userNotif})

@login_required
def AddDesignationSuccess(request,success):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    depTable = designation.objects.all()
    return render(request, 'designationTable.html', {'depTable':depTable, 'success':success, 'userNotif': userNotif})

@login_required
def DeleteDesignation(request,pk):
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    try:
        depTable = designation.objects.get(id=pk)
    except:
        pass
    depTable.delete()
    return redirect(AddDesignationSuccess, success="Deleted")

@login_required
def Department(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    depTable = department.objects.all()
    return render(request, 'departmentTable.html', {'depTable':depTable, 'userNotif': userNotif})

@login_required
def AddDepartmentSuccess(request,success):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    depTable = department.objects.all()
    return render(request, 'departmentTable.html', {'depTable':depTable, 'success':success, 'userNotif': userNotif})

@login_required
def DeleteDepartment(request,pk):
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    try:
        depTable = department.objects.get(id=pk)
    except:
        pass
    depTable.delete()
    return redirect(AddDepartmentSuccess, success="Deleted")

@login_required
def EditDepartment(request,pk):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    try:
        departmentValue = department.objects.get(id=pk)
        initial_dict_department = {
            "Department_Name" : departmentValue.Department_Name,
            "Mail_Alias" : departmentValue.Mail_Alias,
            "Department_Lead" : departmentValue.Department_Lead,
        }
    except:
        initial_dict_department = {}
    if request.method == 'POST':
        departmentForm = DepartmentForm(request.POST, initial = initial_dict_department)
        if departmentForm.is_valid():
            departmentValue.Department_Name = request.POST.get("Department_Name")
            departmentValue.Mail_Alias = request.POST.get("Mail_Alias")
            DepartmentLead = request.POST.get("Department_Lead")
            departmentValue.Department_Lead = User.objects.get(id=DepartmentLead)
            departmentValue.save()
            return redirect(AddDepartmentSuccess, success="Updated")
    else:
        departmentForm = DepartmentForm(initial = initial_dict_department)
    return render(request, 'departmentEdit.html', {'departmentForm':departmentForm, 'userNotif': userNotif})

@login_required
def AddDepartment(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    if request.method == 'POST':
        departmentForm = DepartmentForm(request.POST)
        if departmentForm.is_valid():
            Department_Name = request.POST.get("Department_Name")
            Mail_Alias = request.POST.get("Mail_Alias")
            Department_Lead = request.POST.get("Department_Lead")
            DepartmentLead = User.objects.get(id=Department_Lead)
            user = department.objects.create(Department_Name=Department_Name,Mail_Alias=Mail_Alias, Department_Lead=DepartmentLead)
        # return render(request, 'department.html', {'departmentForm':departmentForm, 'success': True})
            return redirect(AddDepartmentSuccess, success="Added")
    else:
        departmentForm = DepartmentForm()
    return render(request, 'department.html', {'departmentForm':departmentForm, 'userNotif': userNotif})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                dj_login(request, user)
                return redirect('/user/dashboard/')
            else:
                # login(request, user)
                try:
                    userApproved = UserApproved.objects.get(Employee=user)
                    if userApproved.AdminApproved == True:
                        dj_login(request, user)
                        return redirect('/user/dashboard/')
                    else:
                        form = AuthenticationForm(request.POST)
                        valid_user = username + ' needs to be approved by admin'
                        return render(request, 'login.html', {'form': form, 'valid_user':valid_user})
                except:
                    form = AuthenticationForm(request.POST)
                    valid_user = 'Something went wrong! Please try again.'
                    return render(request, 'login.html', {'form': form, 'valid_user':valid_user})
        else:
            form = AuthenticationForm(request.POST)
            valid_user = 'Please Enter Valid Username and Password'
            return render(request, 'login.html', {'form': form, 'valid_user':valid_user})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})



@login_required
def adminDashboard(request):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
        print(userNotif)
    except:
        userNotif = False
    userApproved = UserApproved.objects.filter(AdminApproved=False)
    employeeDetails = Personal.objects.all()
    noOfUser = UserApproved.objects.filter(AdminApproved=True).count()
    totalLeaves = ApplyLeave.objects.filter(Employee=request.user).count()
    totalLeavesApproved = ApplyLeave.objects.filter(Employee=request.user, Approved=True).count()
    totalLeavesRejected = ApplyLeave.objects.filter(Employee=request.user, Rejected=True).count()
    holidayUp = HolidayList.objects.filter(Date__gte=datetime.today().strftime('%Y-%m-%d')).order_by('Date')
    birthdayUp = Personal.objects.filter(Date_Of_Birth__month=datetime.today().month).order_by('Date_Of_Birth')
    leaveReport = LeaveAvailable.objects.filter(employee=request.user)
    leavesApplied = ApplyLeave.objects.filter(Valid_From__gte=datetime.today().strftime('%Y-%m-%d'), Employee=request.user, Approved=True).order_by('-timestamp')
    return render(request, 'adminDashboard.html', {'userApproved': userApproved, 'employeeDetails': employeeDetails, 'noOfUser': noOfUser, 'holidayUp':holidayUp, 'birthdayUp':birthdayUp, 'leaveReport':leaveReport, 'leavesApplied': leavesApplied, 'totalLeaves':totalLeaves, 'totalLeavesApproved': totalLeavesApproved, 'totalLeavesRejected': totalLeavesRejected, 'userNotif': userNotif})

@login_required
def adminDashboardNotAllowed(request, success):
    try:
        userNotif = UserNotification.objects.get(Employee=request.user.id)
    except:
        userNotif = False
    userApproved = UserApproved.objects.filter(AdminApproved=False)
    employeeDetails = Personal.objects.all()
    noOfUser = UserApproved.objects.filter(AdminApproved=True).count()
    totalLeaves = ApplyLeave.objects.filter(Employee=request.user).count()
    totalLeavesApproved = ApplyLeave.objects.filter(Employee=request.user, Approved=True).count()
    totalLeavesRejected = ApplyLeave.objects.filter(Employee=request.user, Rejected=True).count()
    holidayUp = HolidayList.objects.filter(Date__gte=datetime.today().strftime('%Y-%m-%d')).order_by('Date')
    birthdayUp = Personal.objects.filter(Date_Of_Birth__month=datetime.today().month).order_by('Date_Of_Birth')
    leaveReport = LeaveAvailable.objects.filter(employee=request.user)
    leavesApplied = ApplyLeave.objects.filter(Valid_From__gte=datetime.today().strftime('%Y-%m-%d'), Employee=request.user, Approved=True).order_by('-timestamp')
    return render(request, 'adminDashboard.html', {'success':success, 'userApproved': userApproved, 'employeeDetails': employeeDetails, 'noOfUser': noOfUser, 'holidayUp':holidayUp, 'birthdayUp':birthdayUp, 'leaveReport':leaveReport, 'leavesApplied': leavesApplied, 'totalLeaves':totalLeaves, 'totalLeavesApproved': totalLeavesApproved, 'totalLeavesRejected': totalLeavesRejected, 'userNotif': userNotif})

@login_required
def approveUser(request,id):
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    try:
        userApproved = UserApproved.objects.get(id=id)
    except:
        return HttpResponse('no user')
    userApproved.AdminApproved = True
    userApproved.save()
    return redirect(ApproveEmployeeSuccess, success="Approved")


@login_required
def disapproveUser(request,id):
    if request.user.is_superuser == False:
        return redirect(adminDashboardNotAllowed, success="NotAllowed")
    try:
        userApproved = UserApproved.objects.get(id=id)
    except:
        return HttpResponse('no user')
    try:
        user = User.objects.get(id=userApproved.Employee.id)
    except:
        return HttpResponse('no user')
    user.delete()
    userApproved.delete()
    return redirect(ApproveEmployeeSuccess, success="Rejected")