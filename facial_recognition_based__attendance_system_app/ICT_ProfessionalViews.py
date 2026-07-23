from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db import models
import os
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import datetime  # To Parse input DateTime into Python Date Time Object

from .FacialRecognition.mainOrginal import MainClass

from .models import Users, DepartmentHead, BatchInfo, Instructor, Colleges, Departments, Course, \
    Students, \
    SessionYearModel, \
    FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport, MLModel, \
    Dataset, DatasetItem, AssignInstructor, ICT_Professional, \
    RegisterForCourse, StudentStatus, AttendanceWeight, Contact
from .forms import AddStudentForm, EditStudentForm, TestForm, MLForm, EditMLForm, UploadImageForm
from PIL import Image
from numpy import asarray


def admin_home(request):
    # To display the total number of admin, department head, instructor, and student
    all_student_count = Students.objects.all().count()
    admin_count = ICT_Professional.objects.all().count()
    head_count = DepartmentHead.objects.all().count()
    staff_count = Instructor.objects.all().count()

    # To display the total amount of college, and department
    department_count = Departments.objects.all().count()
    college_count = Colleges.objects.all().count()

    # Total Course and students in Each Department
    department_all = Departments.objects.all()
    department_name_list = []
    subjectdep_count_list = []
    studentdep_count_list_in_department = []

    for department in department_all:
        subjects = Course.objects.filter(department_id=department.id).count()
        students = Students.objects.filter(department_id=department.id).count()
        department_name_list.append(department.department_name)
        subjectdep_count_list.append(subjects)
        studentdep_count_list_in_department.append(students)

    # Total students in each subject
    subject_list = []
    student_count_list_in_subject = []
    subjects = Course.objects.all()
    for subject in subjects:
        student_count = RegisterForCourse.objects.filter(subject_id=subject).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    # Initialize variables before staff loop
    count_present_in_department_month = []
    count_absent_in_department_month = []
    department_name_list_month = []
    count_present_in_department_day = []
    count_absent_in_department_day = []
    department_name_list_day = []

    # For Staffs
    staff_attendance_present_list = []
    staff_attendance_leave_list = []
    staff_name_list = []
    subject_ids = []

    staffs = Instructor.objects.all()
    for staff in staffs:
        assignInstructor = AssignInstructor.objects.filter(staff_id=staff.id)
        for assign in assignInstructor:
            subject_id = assign.subject_id
            subject_ids.append(subject_id)

        attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
        staff_attendance_present_list.append(attendance)
        staff_attendance_leave_list.append(leaves)
        staff_name_list.append(staff.admin.first_name + " " + staff.admin.last_name)
        subject_ids = []

    # Now safely process attendance data
    last_object_month = Attendance.objects.all()
    count_month = Attendance.objects.all().count()

    if count_month > 0:
        initial_month = max(count_month - 30, 0)
        last_attendance_month = list(Attendance.objects.values_list('attendance_date', flat=True))[initial_month:]

        departments = Departments.objects.all()
        for department in departments:
            attendance_list = Attendance.objects.filter(
                department_id=department,
                attendance_date__in=last_attendance_month
            )
            present = AttendanceReport.objects.filter(attendance_id__in=attendance_list, status=True).count()
            absent = AttendanceReport.objects.filter(attendance_id__in=attendance_list, status=False).count()
            count_present_in_department_month.append(present)
            count_absent_in_department_month.append(absent)
            department_name_list_month.append(department.department_name)

        # Last 7 days Attendance Report
        initial_day = max(count_month - 7, 0)
        last_attendance_day = list(Attendance.objects.values_list('attendance_date', flat=True))[initial_day:]

        for department in departments:
            attendance_list = Attendance.objects.filter(
                department_id=department,
                attendance_date__in=last_attendance_day
            )
            present = AttendanceReport.objects.filter(attendance_id__in=attendance_list, status=True).count()
            absent = AttendanceReport.objects.filter(attendance_id__in=attendance_list, status=False).count()
            count_present_in_department_day.append(present)
            count_absent_in_department_day.append(absent)
            department_name_list_day.append(department.department_name)

    # For Students
    student_attendance_present_list = []
    student_attendance_leave_list = []
    student_name_list = []

    students = Students.objects.all()
    for student in students:
        attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
        student_attendance_present_list.append(attendance)
        student_attendance_leave_list.append(leaves + absent)
        student_name_list.append(student.admin.first_name)

    context = {
        "all_student_count": all_student_count,
        'department_count': department_count,
        'college_count': college_count,
        "subject_count": head_count,
        "course_count": admin_count,
        "staff_count": staff_count,
        "course_name_list": department_name_list,
        "department_name_list": department_name_list,
        "subjectdep_count_list": subjectdep_count_list,
        "studentdep_count_list_in_department": studentdep_count_list_in_department,
        "subject_list": subject_list,
        "student_count_list_in_subject": student_count_list_in_subject,
        "staff_attendance_present_list": staff_attendance_present_list,
        "count_present_in_department_month": count_present_in_department_month,
        "count_absent_in_department_month": count_absent_in_department_month,
        "department_name_list_month": department_name_list_month,
        "count_present_in_department_day": count_present_in_department_day,
        "count_absent_in_department_day": count_absent_in_department_day,
        "department_name_list_day": department_name_list_day,
    }
    return render(request, "admin_templates/home_content.html", context)



def add_staff(request):
    colleges = Colleges.objects.all()
    departments = Departments.objects.all()
    # courses = Courses.objects.all()
    # LoginRequiredMixin.login_url = 'login'
    context = {
        # "courses": courses,
        "colleges": colleges,
        "departments": departments,
    }
    return render(request, "admin_templates/add_staff_template - Copy.html", context)


def add_staff_save(request):
    if request.method != "POST" and request.FILES['profile']:
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        college_id = request.POST.get('college')

        department_id = request.POST.get('department')

        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        try:
            college = Colleges.objects.get(id=college_id)
            department = Departments.objects.get(id=department_id)

            staffs_obj = Instructor.objects.all()
            flag = True
            for obj in staffs_obj:
                if obj.admin.email == email:
                    flag = False
            if flag:
                user = Users.objects.create_user(username=username, password=password, email=email,
                                                 first_name=first_name, last_name=last_name, user_type=2)
                user.instructor.address = address
                user.instructor.profile_pic = profile_pic_url
                user.instructor.college_id = college
                user.instructor.department_id = department

                user.save()
                messages.success(request, "Staff Added Successfully!")
                return redirect('add_staff')
            else:
                messages.success(request, "Staff already added!")
                return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('add_staff')


def manage_staff(request):
    staffs = Instructor.objects.all()
    # departments = Departments.objects.all()
    # colleges = Colleges.objects.all()
    context = {
        "staffs": staffs,
        # "departments": departments,
        # "colleges": colleges,

    }
    return render(request, "admin_templates/manage_staff_template.html", context)


def edit_staff(request, staff_id):
    staff = Instructor.objects.get(admin=staff_id)
    departments = Departments.objects.all()
    colleges = Colleges.objects.all()
    context = {
        "staff": staff,
        "departments": departments,
        "colleges": colleges,
        "id": staff_id
    }
    return render(request, "admin_templates/edit_staff_template.html", context)


def edit_staff_save(request):
    if request.method != "POST" and request.FILES['profile']:
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        college_id = request.POST.get('college')
        college = Colleges.objects.get(id=college_id)

        department_id = request.POST.get('department')
        department = Departments.objects.get(id=department_id)

        try:
            # INSERTING into Users Model
            user = Users.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username

            user.save()

            # INSERTING into Staff Model
            staff_model = Instructor.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.profile_pic = profile_pic_url
            staff_model.college_id = college
            staff_model.department_id = department
            staff_model.save()

            messages.success(request, "Staff Updated Successfully.")
            return redirect('/edit_staff/' + staff_id)

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_staff/' + staff_id)


def delete_staff(request, staff_id):
    staff = Instructor.objects.get(admin=staff_id)
    try:
        # user = Users.objects.get(id=staff.admin.id)
        staff.delete()
        # user.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_staff')


def add_college(request):
    return render(request, "admin_templates/add_college_template.html")


def add_college_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_college')
    else:
        college = request.POST.get('college')
        try:
            colleges_obj = Colleges.objects.all()
            flag = True
            for obj in colleges_obj:
                if obj.college_name == college:
                    flag = False
            if flag:
                college_model = Colleges(college_name=college)
                college_model.save()
                messages.success(request, "College Added Successfully!")
                return redirect('add_college')
            else:
                messages.success(request, "College already added!")
                return redirect('add_college')
        except:
            messages.error(request, "Failed to Add College!")
            return redirect('add_college')


def manage_college(request):
    colleges = Colleges.objects.all()
    context = {
        "colleges": colleges
    }
    return render(request, 'admin_templates/manage_college_template.html', context)


def edit_college(request, college_id):
    college = Colleges.objects.get(id=college_id)
    context = {
        "college": college,
        "id": college_id
    }
    return render(request, 'admin_templates/edit_college_template.html', context)


def edit_college_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        college_id = request.POST.get('college_id')
        college_name = request.POST.get('college')

        try:
            college = Colleges.objects.get(id=college_id)
            college.college_name = college_name
            college.save()

            messages.success(request, "College Updated Successfully.")
            return redirect('/edit_college/' + college_id)

        except:
            messages.error(request, "Failed to Update College.")
            return redirect('/edit_college/' + college_id)


def delete_college(request, college_id):
    college = Colleges.objects.get(id=college_id)
    try:
        college.delete()
        messages.success(request, "College Deleted Successfully.")
        return redirect('manage_college')
    except:
        messages.error(request, "Failed to Delete College.")
        return redirect('manage_college')


def manage_session(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "admin_templates/manage_session_template.html", context)


def add_session(request):
    return render(request, "admin_templates/add_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("add_session")
        except:
            messages.error(request, "Failed to Add Session Year")
            return redirect("add_session")


def edit_session(request, session_id):
    session_year = SessionYearModel.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "admin_templates/edit_session_template.html", context)


def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect('/edit_session/' + session_id)
        except:
            messages.error(request, "Failed to Update Session Year.")
            return redirect('/edit_session/' + session_id)


def delete_session(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session')


def add_student(request):
    form = AddStudentForm()
    context = {
        "form": form
    }
    return render(request, 'admin_templates/add_student_template.html', context)


def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        form = AddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            id = form.cleaned_data['id']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            session_year_id = form.cleaned_data['session_year_id']
            # course_id = form.cleaned_data['course_id']
            batch = form.cleaned_data['batch_id']
            college_id = form.cleaned_data['college_id']
            department_id = form.cleaned_data['department_id']
            gender = form.cleaned_data['gender']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            # try:
            user = Users.objects.create_user(username=username, password=password, email=email,
                                             first_name=first_name, last_name=last_name, user_type=3)
            user.students.student_id = id
            user.students.address = address

            # course_obj = Courses.objects.get(id=course_id)
            # user.students.course_id = course_obj

            # batch_obj = BatchInfo.objects.get(id=batch_id)
            user.students.batch = int(batch)

            college_obj = Colleges.objects.get(id=college_id)
            user.students.college_id = college_obj

            department_obj = Departments.objects.get(id=department_id)
            user.students.department_id = department_obj

            session_year_obj = SessionYearModel.objects.get(id=session_year_id)
            user.students.session_year_id = session_year_obj

            user.students.gender = gender
            user.students.profile_pic = profile_pic_url
            user.save()
            messages.success(request, "Student Added Successfully!")
            return redirect('add_student')
            # except:
            messages.error(request, "Failed to Add Student!")
            return redirect('add_student')
        else:
            return redirect('add_student')


def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'admin_templates/manage_student_template.html', context)


def edit_student(request, student_id):
    # Adding Student ID into Session Variable
    request.session['student_id'] = student_id

    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = student.admin.email
    form.fields['username'].initial = student.admin.username
    form.fields['id'].initial = student.student_id
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['address'].initial = student.address
    form.fields['batch_id'].initial = student.batch
    # form.fields['course_id'].initial = student.course_id.id
    form.fields['gender'].initial = student.gender
    form.fields['session_year_id'].initial = student.session_year_id.id

    context = {
        "id": student_id,
        "username": student.admin.username,
        "form": form
    }
    return render(request, "admin_templates/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return redirect('/manage_student')

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            id = form.cleaned_data['id']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            batch = form.cleaned_data['batch_id']
            print("error "+batch)
            # course_id = form.cleaned_data['course_id']
            gender = form.cleaned_data['gender']
            session_year_id = form.cleaned_data['session_year_id']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = Users.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Students Table
                student_model = Students.objects.get(admin=student_id)
                student_model.student_id = id
                student_model.address = address

                # batchinfo = BatchInfo.objects.get(id=batch_id)

                student_model.batch = batch

                # course = Courses.objects.get(id=course_id)
                # student_model.course_id = course

                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                student_model.session_year_id = session_year_obj

                student_model.gender = gender
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['student_id']

                messages.success(request, "Student Updated Successfully!")
                return redirect('/edit_student/' + student_id)
        
            except Exception as e:
                print(f"An error occurred: {e}")
                messages.success(request, "Failed to Uupdate Student.")
                return redirect('/edit_student/' + student_id)
        else:
            return redirect('/edit_student/' + student_id)


def delete_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    try:
        # user = Users.objects.get(id=student.admin.id)
        student.delete()
        # user.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


def add_department(request):
    colleges = Colleges.objects.all()
    # staffs = Users.objects.filter(user_type='2')
    context = {
        "colleges": colleges,
        # "staffs": staffs
    }
    return render(request, 'admin_templates/add_department_template.html', context)


def add_department_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_department')
    else:
        department_name = request.POST.get('department')

        college_id = request.POST.get('college')
        college = Colleges.objects.get(id=college_id)

        # staff_id = request.POST.get('staff')
        # staff = Users.objects.get(id=staff_id)
        try:
            departments_obj = Departments.objects.all()
            flag = True
            for obj in departments_obj:
                if obj.department_name == department_name:
                    flag = False
            if flag:
                department = Departments(department_name=department_name, college_id=college)
                department.save()
                messages.success(request, department_name + " Added as Department Successfully!")
                return redirect('add_department')
            else:
                messages.success(request, "Department already added!")
                return redirect('add_department')

        except:
            messages.error(request, "Failed to Add " + department_name + " as Department!")
            return redirect('add_department')


def manage_department(request):
    departments = Departments.objects.all()
    context = {
        "departments": departments
    }
    return render(request, 'admin_templates/manage_department_template.html', context)


def edit_department(request, department_id):
    department = Departments.objects.get(id=department_id)
    colleges = Colleges.objects.all()
    # staffs = Users.objects.filter(user_type='2')
    context = {
        "department": department,
        "colleges": colleges,
        # "staffs": staffs,
        "id": department_id
    }
    return render(request, 'admin_templates/edit_department_template.html', context)


def edit_department_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        department_id = request.POST.get('department_id')
        department_name = request.POST.get('department')
        college_id = request.POST.get('college')
        # staff_id = request.POST.get('staff')

        try:
            department = Departments.objects.get(id=department_id)
            department.department_name = department_name

            college = Colleges.objects.get(id=college_id)
            department.college_id = college

            department.save()

            messages.success(request, department_name + " Updated Successfully.")
            return HttpResponseRedirect(reverse("edit_department", kwargs={"department_id": department_id}))

        except:
            messages.error(request, "Failed to Update " + department_name + ".")
            return HttpResponseRedirect(reverse("edit_department", kwargs={"department_id": department_id}))


def delete_department(request, department_id):
    department = Departments.objects.get(id=department_id)
    try:
        department_name = department.department_name
        department.delete()
        messages.success(request, department_name + " Deleted Successfully.")
        return redirect('manage_department')
    except:
        messages.error(request, "Failed to Update " + department_name + ".")
        return redirect('manage_department')


def add_head(request):
    # head = Head.objects.get(admin=request.user.id)
    colleges = Colleges.objects.all()
    departments = Departments.objects.all()
    staffs = Instructor.objects.all()
    context = {
        "colleges": colleges,
        "departments": departments,
        "staffs": staffs
    }
    return render(request, 'admin_templates/add_head_template.html', context)


def add_head_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_head')
    else:

        username = request.POST.get('username')
        password = request.POST.get('password')

        college_id = request.POST.get('college')
        college = Colleges.objects.get(id=college_id)

        department_id = request.POST.get('department')
        department = Departments.objects.get(id=department_id)

        staff_id = request.POST.get('staff')
        staff = Instructor.objects.get(id=staff_id)
        try:
            staffs_obj = DepartmentHead.objects.all()
            flag = True
            for obj in staffs_obj:
                if obj.department_id == department and obj.college_id == college:
                    flag = False
            if flag:
                user = Users.objects.create_user(username=username, password=password, user_type=4)
                user.departmenthead.college_id = college
                user.departmenthead.department_id = department
                user.departmenthead.staff_id = staff
                user.save()
                messages.success(request,
                                 staff.admin.first_name + " " + staff.admin.last_name + " Added as Head Successfully!")
                return redirect('add_head')
            else:
                messages.success(request, "Head already added!")
                return redirect('add_head')
        except:
            messages.error(request,
                           "Failed to Add " + staff.admin.first_name + " " + staff.admin.last_name + " as Head!")
            return redirect('add_head')


def manage_head(request):
    head = DepartmentHead.objects.all()
    context = {
        "head": head
    }
    return render(request, 'admin_templates/manage_head_template.html', context)


def edit_head(request, head_id):
    heads = DepartmentHead.objects.get(id=head_id)
    colleges = Colleges.objects.all()
    departments = Departments.objects.all()
    staffs = Instructor.objects.filter(department_id=heads.department_id)
    context = {
        "head": heads,
        "colleges": colleges,
        "departments": departments,
        "staffs": staffs,
        "id": head_id
    }
    return render(request, 'admin_templates/edit_head_template.html', context)


def edit_head_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        username = request.POST.get('username')
        head_id = request.POST.get('head_id')
        college_id = request.POST.get('college')
        department_id = request.POST.get('department')
        staff_id = request.POST.get('staff')
        try:
            head = DepartmentHead.objects.get(id=head_id)
            user = Users.objects.get(id=head.admin.id)
            user.username = username
            user.save()
            # INSERTING into head Model
            college = Colleges.objects.get(id=college_id)
            head.college_id = college
            department = Departments.objects.get(id=department_id)
            head.department_id = department
            staff = Instructor.objects.get(id=staff_id)
            head.staff_id = staff
            head.save()
            messages.success(request, "Head Updated Successfully.")
            return HttpResponseRedirect(reverse("edit_head", kwargs={"head_id": head_id}))
        except:
            messages.error(request, " Failed to Update Head.")
            return HttpResponseRedirect(reverse("edit_head", kwargs={"head_id": head_id}))


def delete_head(request, head_id):
    head = DepartmentHead.objects.get(id=head_id)
    try:
        # user = Users.objects.get(id=head.admin.id)
        head.delete()
        # user.delete()
        messages.success(request, "Head Deleted Successfully.")
        return redirect('manage_head')
    except:
        messages.error(request, "Failed to Delete Head.")
        return redirect('manage_head')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = Users.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = Users.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.filter(receiver=request.user.id)
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'admin_templates/student_feedback_template.html', context)


def everyone_feedback_message(request):
    contacts = Contact.objects.all()
    context = {
        "contacts": contacts
    }
    return render(request, 'admin_templates/everyone_feedback_message.html', context)


def delete_everyone_feedback(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    try:
        contact.delete()
        messages.success(request, "Comment Deleted Successfully.")
        return redirect('everyone_feedback_message')
    except:
        messages.error(request, "Failed to Delete Comment.")
        return redirect('everyone_feedback_message')


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.filter(receiver=request.user.id)
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'admin_templates/staff_feedback_template.html', context)


@csrf_exempt
def staff_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def admin_view_attendance(request):
    admin = ICT_Professional.objects.get(admin=request.user.id)
    departments = Departments.objects.all()
    # subjects = Course.objects.all()
    # session_years = SessionYearModel.objects.all()
    context = {
        "departments": departments,
        # "session_years": session_years
    }
    return render(request, "admin_templates/view_attendance.html", context)


def admin_view_final_attendance(request):
    admin = ICT_Professional.objects.get(admin=request.user.id)
    departments = Departments.objects.all()
    # subjects = Course.objects.all()
    # session_years = SessionYearModel.objects.all()
    context = {
        "departments": departments,
        # "session_years": session_years
    }
    return render(request, "admin_templates/admin_view_attendance_final.html", context)


@csrf_exempt
def load_batches(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get("department")
    department = Departments.objects.get(id=department_id)
    registered_courses = RegisterForCourse.objects.filter(department_id=department)
    batches = []
    for course in registered_courses:
        if course.batch not in batches:
            batches.append(course.batch)

    list_data = []

    for batch in batches:
        data_small = {"id": batch,
                      "batch": batch,
                      }
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def load_subjects(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get("department")
    department = Departments.objects.get(id=department_id)
    registered_courses = RegisterForCourse.objects.filter(department_id=department)
    courses = []
    for course in registered_courses:
        if course.subject_id not in courses:
            courses.append(course.subject_id)

    list_data = []
    for course in courses:
        data_small = {"id": course.id,
                      "subject": course.subject_name,
                      }
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def load_batches_final(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get("department")
    subject_id = request.POST.get("subject")
    department = Departments.objects.get(id=department_id)
    subject = Course.objects.get(id=subject_id)
    registered_courses = RegisterForCourse.objects.filter(department_id=department, subject_id=subject)
    batches = []
    for course in registered_courses:
        if course.batch not in batches:
            batches.append(course.batch)

    list_data = []

    for batch in batches:
        data_small = {"id": batch,
                      "batch": batch,
                      }
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def load_sections(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get("department")
    department = Departments.objects.get(id=department_id)
    registered_courses = RegisterForCourse.objects.filter(department_id=department)
    sections = []
    for course in registered_courses:
        if course.section not in sections:
            sections.append(course.section)

    list_data = []

    for section in sections:
        data_small = {"id": section,
                      "section": section,
                      }
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def load_sections_final(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get("department")
    subject_id = request.POST.get("subject")
    department = Departments.objects.get(id=department_id)
    subject = Course.objects.get(id=subject_id)
    registered_courses = RegisterForCourse.objects.filter(department_id=department, subject_id=subject)
    sections = []
    for course in registered_courses:
        if course.section not in sections:
            sections.append(course.section)

    list_data = []

    for section in sections:
        data_small = {"id": section,
                      "section": section,
                      }
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def load_attendance_department(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get("department")
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    department = Departments.objects.get(id=department_id)
    # Parsing the date data into Python object
    start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    attendance_list = Attendance.objects.filter(department_id=department,
                                                attendance_date__range=(start_date_parse, end_date_parse))
    attendance_report = AttendanceReport.objects.filter(attendance_id__in=attendance_list)
    total_present = 0
    total_absent = 0
    for report in attendance_report:
        if report.status:
            total_present = total_present + 1
        else:
            total_absent = total_absent + 1

    list_data = []
    data_small = {"present": total_present,
                  "absent": total_absent,
                  }
    list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get("department")
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    department = Departments.objects.get(id=department_id)
    # Parsing the date data into Python object
    start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    attendance_list = Attendance.objects.filter(department_id=department,
                                                attendance_date__range=(start_date_parse, end_date_parse))
    attendance_report = AttendanceReport.objects.filter(attendance_id__in=attendance_list)
    # Only Passing Student Id and Student Name Only
    list_data = []
    status_list = StudentStatus.objects.all()
    students_list = []
    for status in status_list:
        students_list.append(status.student_id)
    count = 0
    for student in attendance_report:
        if student.student_id not in students_list:
            count = count + 1
            data_small = {"id": count,
                          "student_id": student.student_id.student_id,
                          "name": student.student_id.admin.first_name + " " + student.student_id.admin.last_name,
                          "date": str(student.attendance_id.attendance_date),
                          "subject": student.attendance_id.subject_id.subject_name,
                          "type": student.attendance_id.attendance_type,
                          "status": student.status,
                          }
            list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_view_final_taking_list(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get('department')
    section = request.POST.get('section')
    batch = request.POST.get('batch')
    subject_id = request.POST.get('subject')
    attendance_type = request.POST.get('attendance_type')
    subject = Course.objects.get(id=subject_id)
    department = Departments.objects.get(id=department_id)

    attendance_lecture = Attendance.objects.filter(section=section, batch=batch, subject_id=subject,
                                                   department_id=department, attendance_type='lecture')
    attendance_lab = Attendance.objects.filter(section=section, batch=batch, subject_id=subject,
                                               department_id=department, attendance_type='lab_class')
    total_lecture_attendance = attendance_lecture.count()
    total_lab_attendance = attendance_lab.count()

    total_attendance_lecture = AttendanceReport.objects.filter(attendance_id__in=attendance_lecture)
    total_attendance_lab = AttendanceReport.objects.filter(attendance_id__in=attendance_lab)

    attendance_all = Attendance.objects.filter(section=section, batch=batch, subject_id=subject,
                                               department_id=department)
    attendance_report_all = AttendanceReport.objects.filter(attendance_id__in=attendance_all)

    total_student_list = []

    for attendance in attendance_report_all:
        if attendance.student_id not in total_student_list:
            total_student_list.append(attendance.student_id)

    attendance_count_lecture = 0
    attendance_count_lab = 0
    student_data_lecture = []
    student_data_lab = []
    check = 0
    for student in total_student_list:
        for attendance in total_attendance_lecture:
            if student.id == attendance.student_id.id and attendance.status:
                attendance_count_lecture = attendance_count_lecture + 1
        data_small_lecture = {student.id: attendance_count_lecture}
        attendance_count_lecture = 0
        student_data_lecture.append(data_small_lecture)
        for attendance in total_attendance_lab:
            if student.id == attendance.student_id.id and attendance.status:
                attendance_count_lab = attendance_count_lab + 1
        data_small_lab = {student.id: attendance_count_lab}
        attendance_count_lab = 0
        student_data_lab.append(data_small_lab)

    attendance_weight = AttendanceWeight.objects.filter(department_id=department, batch=batch,
                                                        subject_id=subject)
    # lecture_weight = attendance_weight[0].lecturer_class
    # lab_weight = attendance_weight[0].lab_class
    lecture_weight = 0
    lab_weight = 0
    for weight in attendance_weight:
        lecture_weight = weight.lecturer_class
        lab_weight = weight.lab_class

    mandatory_lecture = (total_lecture_attendance * lecture_weight) / 100
    mandatory_lab = (total_lab_attendance * lab_weight) / 100

    lecture_final_taker = []
    lecture_final_not_taker = []
    lab_final_taker = []
    lab_final_not_taker = []
    for student_data in student_data_lecture:
        for student_id, count in student_data.items():
            student = Students.objects.get(id=student_id)
            if count >= mandatory_lecture:
                lecture_final_taker.append(student)
            else:
                lecture_final_not_taker.append(student)
    for student_data in student_data_lab:
        for student_id, count in student_data.items():
            student = Students.objects.get(id=student_id)
            if count >= mandatory_lab:
                lab_final_taker.append(student)
            else:
                lab_final_not_taker.append(student)
    final_taking_student_list = []
    final_not_taking_student_list = []
    for student in lecture_final_taker:
        if student in lab_final_taker:
            final_taking_student_list.append(student)
        else:
            final_not_taking_student_list.append(student)

    total_final_not_taker_list = lecture_final_not_taker + lab_final_not_taker + final_not_taking_student_list
    # Only Passing Student Id and Student Name Only
    status_list = StudentStatus.objects.all()
    students_list = []
    for status in status_list:
        students_list.append(status.student_id)
    list_data = []
    students = []
    amount = 0
    if attendance_type == 'non_final':
        for student in total_final_not_taker_list:
            if student not in students_list and student not in students:
                amount = amount + 1
                data_small = {"id": amount,
                              "student_id": student.student_id,
                              "name": student.admin.first_name + " " + student.admin.last_name
                              }
                list_data.append(data_small)
                students.append(student)
    if attendance_type == 'final':
        for student in final_taking_student_list:
            if student not in students_list:
                amount = amount + 1
                data_small = {"id": amount,
                              "student_id": student.student_id,
                              "name": student.admin.first_name + " " + student.admin.last_name
                              }
                list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_student_batch(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get("department")
    batch = request.POST.get("batch")
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    department = Departments.objects.get(id=department_id)
    # Parsing the date data into Python object
    start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    attendance_list = Attendance.objects.filter(department_id=department, batch=batch,
                                                attendance_date__range=(start_date_parse, end_date_parse))
    attendance_report = AttendanceReport.objects.filter(attendance_id__in=attendance_list)
    # Only Passing Student Id and Student Name Only
    list_data = []
    status_list = StudentStatus.objects.all()
    students_list = []
    for status in status_list:
        students_list.append(status.student_id)

    count = 0
    for student in attendance_report:
        if student.student_id not in students_list:
            count = count + 1
            data_small = {"id": count,
                          "student_id": student.student_id.student_id,
                          "name": student.student_id.admin.first_name + " " + student.student_id.admin.last_name,
                          "date": str(student.attendance_id.attendance_date),
                          "subject": student.attendance_id.subject_id.subject_name,
                          "type": student.attendance_id.attendance_type,
                          "status": student.status,
                          }
            list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_student_section(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get("department")
    batch = request.POST.get("batch")
    section = request.POST.get("section")
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    department = Departments.objects.get(id=department_id)
    # Parsing the date data into Python object
    start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    attendance_list = Attendance.objects.filter(department_id=department, batch=batch, section=section,
                                                attendance_date__range=(start_date_parse, end_date_parse))
    attendance_report = AttendanceReport.objects.filter(attendance_id__in=attendance_list)
    # Only Passing Student Id and Student Name Only
    list_data = []
    status_list = StudentStatus.objects.all()
    students_list = []
    for status in status_list:
        students_list.append(status.student_id)

    count = 0
    for student in attendance_report:
        if student.student_id not in students_list:
            count = count + 1
            data_small = {"id": count,
                          "student_id": student.student_id.student_id,
                          "name": student.student_id.admin.first_name + " " + student.student_id.admin.last_name,
                          "date": str(student.attendance_id.attendance_date),
                          "subject": student.attendance_id.subject_id.subject_name,
                          "type": student.attendance_id.attendance_type,
                          "status": student.status,
                          }
            list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def load_attendance_batch(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get("department")
    batch = request.POST.get("batch")
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    department = Departments.objects.get(id=department_id)
    # Parsing the date data into Python object
    start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    attendance_list = Attendance.objects.filter(department_id=department, batch=batch,
                                                attendance_date__range=(start_date_parse, end_date_parse))
    attendance_report = AttendanceReport.objects.filter(attendance_id__in=attendance_list)
    total_present = 0
    total_absent = 0
    for report in attendance_report:
        if report.status:
            total_present = total_present + 1
        else:
            total_absent = total_absent + 1

    list_data = []
    data_small = {"present": total_present,
                  "absent": total_absent,
                  }
    list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def load_attendance_section(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get("department")
    batch = request.POST.get("batch")
    section = request.POST.get("section")
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    department = Departments.objects.get(id=department_id)
    # Parsing the date data into Python object
    start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    attendance_list = Attendance.objects.filter(department_id=department, batch=batch, section=section,
                                                attendance_date__range=(start_date_parse, end_date_parse))
    attendance_report = AttendanceReport.objects.filter(attendance_id__in=attendance_list)
    total_present = 0
    total_absent = 0
    for report in attendance_report:
        if report.status:
            total_present = total_present + 1
        else:
            total_absent = total_absent + 1

    list_data = []
    data_small = {"present": total_present,
                  "absent": total_absent,
                  }
    list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_dates(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Course
    # Getting all data from subject model based on subject_id
    subject_model = Course.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(subject_id=subject_model, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date),
                      "session_year_id": attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


# @csrf_exempt
# def admin_get_attendance_student(request):
#     # Getting Values from Ajax POST 'Fetch Student'
#     attendance_date = request.POST.get('attendance_date')
#     attendance = Attendance.objects.get(id=attendance_date)
#
#     attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
#     # Only Passing Student Id and Student Name Only
#     list_data = []
#
#     for student in attendance_data:
#         data_small = {"id": student.student_id.admin.id,
#                       "name": student.student_id.admin.first_name + " " + student.student_id.admin.last_name,
#                       "status": student.status}
#         list_data.append(data_small)
#
#     return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = Users.objects.get(id=request.user.id)
    context = {
        "user": user
    }
    return render(request, 'admin_templates/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST" and request.FILES['profile']:
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        try:
            customuser = Users.objects.get(id=request.user.id)
            customuser.username = username
            customuser.email = email
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            admin = ICT_Professional.objects.get(admin=request.user.id)
            admin.profile_pic = profile_pic_url
            admin.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')


def staff_profile(request):
    pass


def student_profile(requtest):
    pass


# Dependent Dropdown List
@csrf_exempt
def load_departments(request):
    if request.method == "POST":
        college_id = request.POST['college_id']
        # try:
        college = Colleges.objects.get(id=college_id)
        departments = Departments.objects.filter(college_id=college)
        list_data = []
        for department in departments:
            data_small = {"id": department.id,
                          "name": department.department_name,
                          }
            list_data.append(data_small)
        # except Exception:
        # data['error_message'] = 'error'
        # return JsonResponse(data)
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def load_staffs(request):
    if request.method == "POST":
        department_id = request.POST['department']
        # try:
        department = Departments.objects.get(id=department_id)
        staffs = Instructor.objects.filter(department_id=department)
        list_data = []
        for staff in staffs:
            data_small = {"id": staff.id,
                          "name": staff.admin.first_name + " " + staff.admin.last_name,
                          }
            list_data.append(data_small)
        # except Exception:
        # data['error_message'] = 'error'
        # return JsonResponse(data)
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


# Facial Recognition
def test_image(request):
    form = TestForm()
    context = {
        "form": form
    }
    return render(request, 'admin_templates/predict_image_template.html', context)


def perform_test_image(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('predict_image')
    else:
        form = TestForm(request.POST, request.FILES)
        if form.is_valid():
            #
            # if len(request.FILES) != 0:
            #     model_weight = request.FILES['model_weight']
            #     fs = FileSystemStorage()
            #     filename = fs.save(model_weight.name, model_weight)
            #     model_weight_url = fs.url(filename)
            # else:
            #     model_weight_url = form.cleaned_data['model_weight_list']

            image = form.cleaned_data.get("image")
            # load the image
            image = Image.open(image)
            # convert image to numpy array
            data = asarray(image)

            try:
                result = MainClass.make_predication(data)
                if not result:
                    messages.success(request, 'This Person or Class  is not trained!')
                else:
                    messages.success(request, 'Prediction Result: ' + result)
                return redirect('predict_image')
                # for result in MainClass.make_predication(data, model_weight_url):
            # for result in MainClass.make_predication(data):
            #     try:
            #         # if result
            #         messages.success(request, 'Prediction Result: ' + str(float(result)))
            #     except:
            #         for x in result:
            #             messages.success(request, 'Prediction Result: ' + str(float(x)))
            #
            # return redirect('predict_image')

            except:

                messages.error(request, 'The image is incompatible with the machine learning model')

                return redirect('predict_image')
        else:
            return redirect('predict_image')


def train_model(request):
    form = MLForm()
    context = {
        "form": form
    }
    return render(request, 'admin_templates/train_model_template.html', context)


def perform_train_model(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('train_model')
    else:
        form = MLForm(request.POST, request.FILES)
        if form.is_valid():
            model_name = form.cleaned_data['model_name']
            batch_size = form.cleaned_data['batchSize']
            epoch = form.cleaned_data['epoch']
            number_of_classes = MainClass.get_number_of_class_samples()
            if len(request.FILES) != 0:
                model_weight = request.FILES['model_weight']
                fs = FileSystemStorage()
                filename = fs.save(model_weight.name, model_weight)
                model_weight_url = fs.url(filename)
            else:
                model_weight_url = None
            try:
                mlmodel = MLModel(name=model_name, batchSize=batch_size, epochs=epoch,
                                  number_of_classes=number_of_classes[0], model_weight=model_weight_url)
                mlmodel.save()

                messages.success(request, 'The Model training may take a while !')

            except:
                messages.error(request, 'The model  is not uploaded !')

                return redirect('train_model')
            try:

                MainClass.train_model(epoch=epoch, batch=batch_size)

                messages.success(request, 'The Model is Trained')

                return redirect('train_model')

            except:

                messages.error(request, 'There is a problem with training the Model !')

                return redirect('train_model')
        else:
            return redirect('train_model')


def manage_train_model(request):
    mlmodel = MLModel.objects.all()
    context = {
        "mlmodel": mlmodel,
    }
    return render(request, 'admin_templates/manage_train_model_template.html', context)


def edit_training_parameters(request, model_id):
    # Adding Model ID into Session Variable
    request.session['model_id'] = model_id

    mlmodel = MLModel.objects.get(id=model_id)
    form = EditMLForm()
    # Filling the form with Data from Database
    form.fields['model_name'].initial = mlmodel.name
    form.fields['epoch'].initial = mlmodel.epochs
    form.fields['batchSize'].initial = mlmodel.batchSize
    form.fields['number_of_classes'].initial = mlmodel.number_of_classes

    context = {
        "id": model_id,
        # "username": student.admin.username,
        "form": form
    }
    return render(request, "admin_templates/edit_training_parameters.html", context)


def edit_training_parameters_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        model_id = request.session.get('model_id')
        if model_id == None:
            return redirect('/manage_train_model')

        form = EditMLForm(request.POST, request.FILES)
        if form.is_valid():
            model_name = form.cleaned_data['model_name']
            batch_size = form.cleaned_data['batchSize']
            epoch = form.cleaned_data['epoch']
            number_of_classes = MainClass.get_number_of_class_samples()

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                model_weight = request.FILES['model_weight']
                fs = FileSystemStorage()
                filename = fs.save(model_weight.name, model_weight)
                model_weight_url = fs.url(filename)
            else:
                model_weight_url = None

            try:
                # Then Update MLModel Table
                ml_model = MLModel.objects.get(id=model_id)
                ml_model.name = model_name
                ml_model.epochs = epoch
                ml_model.batchSize = batch_size
                ml_model.number_of_classes = number_of_classes[0]

                if model_weight_url != None:
                    ml_model.model_weight = model_weight_url
                ml_model.save()

            except:
                messages.error(request, "Failed to Update Parameters.")
                return redirect('/edit_training_parameters/' + model_id)
            try:

                MainClass.train_model(epoch=epoch, batch=batch_size)

                # Delete model_id SESSION after the data is updated
                del request.session['model_id']

                messages.success(request, 'The Model is Trained')

                return redirect('/edit_training_parameters/' + model_id)

            except:

                messages.error(request, 'There is a problem with training the Model !')

                return redirect('/edit_training_parameters/' + model_id)
        else:
            return redirect('/edit_training_parameters/' + model_id)


def delete_training_parameters(request, model_id):
    ml_model = MLModel.objects.get(id=model_id)
    try:
        ml_model.delete()
        messages.success(request, "The Training Parameters are Deleted Successfully.")
        return redirect('manage_train_model')
    except:
        messages.error(request, "Failed to Delete the Training Parameters.")
        return redirect('manage_train_model')


def upload_dataset(request):
    form = UploadImageForm()
    context = {
        'form': form
    }
    return render(request, 'admin_templates/upload_dataset_template.html', context)


def upload_dataset_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('upload_dataset')
    else:
        form = UploadImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image_dataset')
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            directory = '' + student_id
            parent_dir = 'Media/ImageDataset/'
            path = os.path.join(parent_dir, directory)
            flag = False
            try:
                os.mkdir(path)
                flag = True
            except:
                flag = False
            try:
                student = Students.objects.get(student_id=student_id)
                dataset1 = Dataset()
                if flag:
                    dataset = Dataset(student_id=student)
                    dataset1 = dataset
                    dataset1.save()
                else:
                    dataset = Dataset.objects.get(student_id=student_id)
                    dataset1 = dataset

                for f in files:
                    dataset_item = DatasetItem(path_to_dir=path, image=f,
                                               dataset=dataset1)  # Do something with each file.
                    dataset_item.save()
                messages.success(request, 'The dataset is uploaded !')

                return redirect('upload_dataset')
            except:
                messages.error(request, 'The dataset is not uploaded !')

            return redirect('upload_dataset')
        else:
            return redirect('upload_dataset')


def manage_uploaded_dataset(request):
    dataset = Dataset.objects.all()
    dataset_item = DatasetItem.objects.all()
    context = {
        "dataset": dataset,
        "dataset_item": dataset_item,
    }
    return render(request, 'admin_templates/manage_uploaded_dataset_template.html', context)


def delete_uploaded_dataset(request, dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)
    datasetitem = DatasetItem.objects.filter(id=dataset_id)
    try:
        dataset.delete()
        datasetitem.delete()
        messages.success(request, "The Uploaded Dataset is Deleted Successfully!")
        return redirect('manage_uploaded_dataset')
    except:
        messages.error(request, "Failed to Delete the Uploaded Dataset!")
        return redirect('manage_uploaded_dataset')
