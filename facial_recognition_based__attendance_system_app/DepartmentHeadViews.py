from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from django.contrib.auth.decorators import login_required
from .models import Course

from .models import (
    Users, Instructor, RegisterForCourse, BatchInfo, Departments,
    Course, SessionYearModel,
    FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff,
    Attendance, AttendanceReport, DepartmentHead, AssignInstructor,
    StudentStatus, AttendanceWeight,
    Students, 
)





def head_home(request):
    try:
        head = DepartmentHead.objects.get(admin=request.user.id)
    except:
        messages.error(request, "Failed to Login!")
        return redirect('login')
    all_student_count = Students.objects.filter(department_id=head.department_id).count()
    subject_count = Course.objects.filter(department_id=head.department_id).count()
    subjects = Course.objects.filter(department_id=head.department_id)
    batches = []
    for subject in subjects:
        if subject.batch not in batches:
            batches.append(subject.batch)
    batch_count = len(batches)
    # course_count = Courses.objects.all().count()
    staff_count = Instructor.objects.filter(department_id=head.department_id).count()
    staffs = Instructor.objects.filter(department_id=head.department_id)

    batch_name_list = []
    subject_count_list = []
    student_count_list_in_batch = []

    for batch in batches:
        subjects = Course.objects.filter(batch=batch, department_id=head.department_id).count()
        students = Students.objects.filter(batch=batch, department_id=head.department_id).count()
        batch_name_list.append(batch)
        subject_count_list.append(subjects)
        student_count_list_in_batch.append(students)

    subject_list = []
    student_count_list_in_subject = []
    subjects = Course.objects.filter(department_id=head.department_id)
    for subject in subjects:
        student_count = RegisterForCourse.objects.filter(subject_id=subject).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    # For Instructor
    staff_attendance_present_list = []
    staff_attendance_leave_list = []
    staff_name_list = []
    subject_ids = []
    # staffs = Instructor.objects.all()
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

    # for each subjects
    last_id = Attendance.objects.filter(department_id=head.department_id)
    count = Attendance.objects.filter(department_id=head.department_id).count()
    initial = count - 7
    last_id_ = []
    check = 0
    for last in last_id:
        check = check + 1
        if check >= initial:
            last_id_.append(last.attendance_date)

    # last_id = Attendance.objects.all()
    # initial = last_id - 3
    # id_list = []
    # for x in range(initial, last_id):
    #     id_list.append(x)
    count_present_in_subject = []
    count_absent_in_subject = []
    subject_name_list = []
    # check = len(id_list)
    subjects = Course.objects.filter(department_id=head.department_id)
    for subject in subjects:
        attendance_list = Attendance.objects.filter(subject_id=subject, attendance_date__in=last_id_)
        # present = len(attendance_list)
        present = AttendanceReport.objects.filter(attendance_id__in=attendance_list, status=True).count()
        absent = AttendanceReport.objects.filter(attendance_id__in=attendance_list, status=False).count()

        count_present_in_subject.append(present)
        count_absent_in_subject.append(absent)
        subject_name_list.append(subject.subject_name)

        # for each subjects
    last_object_month = Attendance.objects.filter(department_id=head.department_id)
    count_month = Attendance.objects.filter(department_id=head.department_id).count()
    initial_month = count_month - 30
    last_attendance_month = []
    flag = 0
    for last in last_object_month:
        flag = flag + 1
        if flag >= initial_month:
            last_attendance_month.append(last.attendance_date)

    # last_id = Attendance.objects.all()
    # initial = last_id - 3
    # id_list = []
    # for x in range(initial, last_id):
    #     id_list.append(x)
    count_present_in_subject_month = []
    count_absent_in_subject_month = []
    subject_name_list_month = []
    # check = len(id_list)
    subjects = Course.objects.filter(department_id=head.department_id)
    for subject in subjects:
        attendance_list = Attendance.objects.filter(subject_id=subject, attendance_date__in=last_attendance_month)
        # present = len(attendance_list)
        present = AttendanceReport.objects.filter(attendance_id__in=attendance_list, status=True).count()
        absent = AttendanceReport.objects.filter(attendance_id__in=attendance_list, status=False).count()
        count_present_in_subject_month.append(present)
        count_absent_in_subject_month.append(absent)
        subject_name_list_month.append(subject.subject_name)
    # For Students
    student_attendance_present_list = []
    student_attendance_leave_list = []
    student_name_list = []

    students = Students.objects.filter(department_id=head.department_id)

    for student in students:
        attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
        student_attendance_present_list.append(leaves + attendance)
        student_attendance_leave_list.append(absent)
        student_name_list.append(student.admin.first_name)

    context = {
        "all_student_count": all_student_count,
        "subject_count": subject_count,
        "course_count": batch_count,
        "staff_count": staff_count,
        "course_name_list": batch_name_list,
        "subject_count_list": subject_count_list,
        "student_count_list_in_course": student_count_list_in_batch,
        "subject_list": subject_list,
        "student_count_list_in_subject": student_count_list_in_subject,
        # "staff_attendance_present_list": staff_attendance_present_list,
        "count_present_in_subject": count_present_in_subject,
        # "staff_attendance_leave_list": staff_attendance_leave_list,
        "count_absent_in_subject": count_absent_in_subject,
        # "staff_name_list": staff_name_list,
        "subject_name_list": subject_name_list,
        # "student_attendance_present_list": student_attendance_present_list,
        # "student_attendance_leave_list": student_attendance_leave_list,
        # "student_name_list": student_name_list,
        "count_present_in_subject_month": count_present_in_subject_month,
        "count_absent_in_subject_month": count_absent_in_subject_month,
        "subject_name_list_month": subject_name_list_month,
    }
    return render(request, "head_template/home_content.html", context)


# Batch Views
def add_batch(request):
    return render(request, "head_template/add_batch_template.html")


def add_batch_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('head_add_batch')
    else:
        batch = request.POST.get('batch')
        section = request.POST.get('section')

        try:
            batches_obj = BatchInfo.objects.all()
            flag = True
            for obj in batches_obj:
                if obj.section == section and obj.batch_name == batch:
                    flag = False
            if flag:
                batch_model = BatchInfo(batch_name=batch, section=section)
                batch_model.save()
                messages.success(request, "Batch Added Successfully!")
                return redirect('head_add_batch')
            else:
                messages.success(request, "Batch Already Existed!")
                return redirect('head_add_batch')
        except:
            messages.error(request, "Failed to Add Batch!")
            return redirect('head_add_batch')


def manage_batch(request):
    batchs = BatchInfo.objects.all()
    context = {
        "batchs": batchs
    }
    return render(request, 'head_template/manage_batch_template.html', context)


def edit_batch(request, batch_id):
    batch = BatchInfo.objects.get(id=batch_id)
    context = {
        "batch": batch,
        "id": batch_id
    }
    return render(request, 'head_template/edit_batch_template.html', context)


def edit_batch_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        batch_id = request.POST.get('batch_id')
        batch_name = request.POST.get('batch')
        section_id = request.POST.get('section')

        try:
            batch = BatchInfo.objects.get(id=batch_id)
            batch.batch_name = batch_name
            batch.section = section
            batch.save()

            messages.success(request, "Batch Updated Successfully.")
            return redirect('/head/edit_batch/' + batch_id)

        except:
            messages.error(request, "Failed to Update Batch.")
            return redirect('/head/edit_batch/' + batch_id)


def delete_batch(request, batch_id):
    batch = BatchInfo.objects.get(id=batch_id)
    try:
        batch.delete()
        messages.success(request, "Batch Deleted Successfully.")
        return redirect('head_manage_batch')
    except:
        messages.error(request, "Failed to Delete Batch.")
        return redirect('head_manage_batch')


def manage_attendance_weight(request):
    head = DepartmentHead.objects.get(admin=request.user.id)
    attendance_weight = AttendanceWeight.objects.filter(department_id=head.department_id)
    context = {
        "attendance_weight": attendance_weight
    }
    return render(request, "head_template/manage_session_template.html", context)


def add_attendance_weight(request):
    head = DepartmentHead.objects.get(admin=request.user.id)
    departments = Departments.objects.all()
    subjects = Course.objects.filter(department_id=head.department_id)
    batch_list = []
    for batch in subjects:
        if batch.batch not in batch_list:
            batch_list.append(batch.batch)
    context = {
        "batch_list": batch_list,
        "subjects": subjects
    }
    return render(request, "head_template/add_session_template.html", context)


def add_attendance_weight_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('head_add_session')
    else:
        head = DepartmentHead.objects.get(admin=request.user.id)
        batch = request.POST.get('batch')
        subject_id = request.POST.get('subject')
        subject = Course.objects.get(id=subject_id)
        lab_class = request.POST.get('lab_class')
        lecturer_class = request.POST.get('lecture_class')

        try:
            weight = AttendanceWeight(batch=batch, department_id=head.department_id, subject_id=subject,
                                      lab_class=lab_class, lecturer_class=lecturer_class)
            weight.save()
            messages.success(request, "Attendance Weight added Successfully!")
            return redirect("head_add_session")
        except:
            messages.error(request, "Failed to Add Attendance Weight")
            return redirect("head_add_session")


def edit_attendance_weight(request, weight_id):
    head = DepartmentHead.objects.get(admin=request.user.id)
    subjects = Course.objects.filter(department_id=head.department_id)
    attendance_weight = AttendanceWeight.objects.get(id=weight_id)
    context = {
        "attendance_weight": attendance_weight,
        "subjects": subjects
    }
    return render(request, "head_template/edit_session_template.html", context)


def edit_attendance_weight_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('head_manage_session')
    else:
        weight_id = request.POST.get('weight_id')
        subject_id = request.POST.get('subject')
        subject = Course.objects.get(id=subject_id)
        lab_class = request.POST.get('lab_class')
        lecturer_class = request.POST.get('lecture_class')

        try:
            weight = AttendanceWeight.objects.get(id=weight_id)
            weight.subject_id = subject
            weight.lab_class = lab_class
            weight.lecturer_class = lecturer_class
            weight.save()

            messages.success(request, "Attendance Weight Updated Successfully.")
            return redirect('/edit_session/' + weight_id)
        except:
            messages.error(request, "Failed to Update Attendance Weight.")
            return redirect('/edit_session/' + weight_id)


def delete_attendance_weight(request, weight_id):
    weight = AttendanceWeight.objects.get(id=weight_id)
    try:
        weight.delete()
        messages.success(request, "Attendance Weight Deleted Successfully.")
        return redirect('head_manage_session')
    except:
        messages.error(request, "Failed to Delete Attendance Weight.")
        return redirect('head_manage_session')


# Register For Course Views
def register_for_course(request):
    head = DepartmentHead.objects.get(admin=request.user.id)
    departments = Departments.objects.all()
    subjects = Course.objects.filter(department_id=head.department_id)
    batch_lists = BatchInfo.objects.all()
    batch_name_list_ = []
    section_name_list_ = []
    for batch_list in batch_lists:
        if batch_list.batch_name not in batch_name_list_:
            batch_name_list_.append(batch_list.batch_name)
        if batch_list.section not in section_name_list_:
            section_name_list_.append(batch_list.section)

    # for subject in subjects:
    #     if subject.batch_id not in bath_list:
    #         bath_list.append(subject.batch_id)

    students = Students.objects.all()
    context = {

        "head": head,
        "departments": departments,
        "students": students,
        "subjects": subjects,
        "batchinfos": batch_name_list_,
        "sections": section_name_list_,

    }
    return render(request, 'head_template/register_for_course_template.html', context)


@csrf_exempt
def register_for_course_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('register_for_course')
    else:
        try:
            department_id = request.POST.get('department')
            department = Departments.objects.get(id=department_id)

            # student_id = request.POST.get('student')
            # student = Students.objects.get(id=student_id)

            subject_ids = request.POST.get('subject')
            student_ids = request.POST.get('student')
            # subject = Course.objects.get(id=subject_id)

            section = request.POST.get('section')
            # batchinfo = BatchInfo.objects.get(id=batch_id)

            semester = request.POST.get('semester')
            batch = request.POST.get('batch')
            curicullem = request.POST.get('curricclum')
            # registerd_students = RegisterForCourse.objects.filter(batch=batch, semester=semester)

            # staff_id = request.POST.get('staff')
            # staff = Users.objects.get(id=staff_id)
            json_student = json.loads(student_ids)
            registerd_students = []
            flag = False

            for student_id in json_student:
                # Attendance of Individual Student saved on AttendanceReport Model
                if student_id['status'] == 1:
                    student = Students.objects.get(id=student_id['id'])
                    registerd_student = RegisterForCourse.objects.filter(student_id=student, batch=batch,
                                                                         semester=semester)
                    registerd_students.append(registerd_student)

            subject_list = []
            for registerd_student in registerd_students:
                for student in registerd_student:
                    subject_list.append(student.subject_id)

            json_subject = json.loads(subject_ids)
            for student_id in json_student:
                # Attendance of Individual Student saved on AttendanceReport Model
                if student_id['status'] == 1:
                    student = Students.objects.get(id=student_id['id'])
                    for subject_id in json_subject:
                        # Attendance of Individual Student saved on AttendanceReport Model
                        if subject_id['status'] == 1:
                            subject = Course.objects.get(id=subject_id['id'])
                            if subject not in subject_list:
                                flag = True
                                registerForCourse = RegisterForCourse(department_id=department, student_id=student,
                                                                      subject_id=subject,
                                                                      section=section, batch=batch, semester=semester,
                                                                      curicullem=curicullem)
                                registerForCourse.save()
            if flag:
                return HttpResponse("OK")
            else:
                return HttpResponse("existed")
        except:
            return HttpResponse("Error")


# WE don't need csrf_token when using Ajax
@csrf_exempt
def head_get_students(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get("department")
    # section = request.POST.get("section")
    batch = request.POST.get("batch")

    department_model = Departments.objects.get(id=department_id)
    # sections = BatchInfo.objects.filter(id=section, batch_name=batch)
    # sections = BatchInfo.objects.get(batch_name=batch)

    # student_list = []
    # for section in sections:
    #     student = Students.objects.filter(department_id=department_model,
    #                                       batch_id=section)
    #     student_list.append(student)

    student_list = Students.objects.filter(department_id=department_model,
                                           batch=int(batch))

    students_list = []
    for student in student_list:
        students_list.append(student)

    # session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []
    for student in students_list:
        data_small = {"id": student.id,
                      "name": student.student_id + ": " + student.admin.first_name + " " + student.admin.last_name}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def manage_register_for_course(request):
    head = DepartmentHead.objects.get(admin=request.user.id)
    registerForCourse = RegisterForCourse.objects.filter(department_id=head.department_id)
    context = {
        "registerforcourses": registerForCourse,
    }
    return render(request, 'head_template/manage_register_for_course_template.html', context)


def edit_register_for_course(request, register_id):
    registerForCourse = RegisterForCourse.objects.get(id=register_id)
    students = Students.objects.all()
    subjects = Course.objects.all()
    departments = Departments.objects.all()
    batchinfos = BatchInfo.objects.all()
    context = {
        "registerforcourse": registerForCourse,
        "students": students,
        "subjects": subjects,
        "batchinfos": batchinfos,
        "departments": departments,
        "id": register_id
    }
    return render(request, 'head_template/edit_register_for_course_template.html', context)


def edit_register_for_course_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        register_id = request.POST.get('register_id')
        section = request.POST.get('section')
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        department_id = request.POST.get('department')
        semester = request.POST.get('semester')
        batch = request.POST.get('batch')
        curicullem = request.POST.get('curricclum')
        try:
            registerForCourse = RegisterForCourse.objects.get(id=register_id)

            registerForCourse.semester = semester
            registerForCourse.batch = batch
            registerForCourse.curicullem = curicullem

            # batchinfo = BatchInfo.objects.get(id=section)
            registerForCourse.section = section

            department = Departments.objects.get(id=department_id)
            registerForCourse.department_id = department

            student = Students.objects.get(id=student_id)
            registerForCourse.student_id = student

            subject = Course.objects.get(id=subject_id)
            registerForCourse.subject_id = subject

            registerForCourse.save()

            messages.success(request, "Register for Course Updated Successfully.")
            # return redirect('/edit_department/'+department_id)
            return HttpResponseRedirect(reverse("edit_register_for_course", kwargs={"register_id": register_id}))

        except:
            messages.error(request, "Failed to Update Register for Course.")
            return HttpResponseRedirect(reverse("edit_register_for_course", kwargs={"register_id": register_id}))
            # return redirect('/edit_department/'+department_id)


def delete_register_for_course(request, register_id):
    registerForCourse = RegisterForCourse.objects.get(id=register_id)
    try:
        registerForCourse.delete()
        messages.success(request, "Register for Course Deleted Successfully.")
        return redirect('manage_register_for_course')
    except:
        messages.error(request, "Failed to Delete Register for Course.")
        return redirect('manage_register_for_course')


def set_student_status(request):
    head = DepartmentHead.objects.get(admin=request.user.id)
    students = []
    try:
        students = RegisterForCourse.objects.filter(department_id=head.department_id)
    except:
        students = []
    students_list = []
    for student in students:
        if student.student_id not in students_list:
            students_list.append(student.student_id)
    context = {
        "students": students_list
    }
    return render(request, "head_template/student_status.html", context)


def student_status_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('set_student_status')
    else:
        student_id = request.POST.get('student')
        student_status = request.POST.get('student_status')
        student = Students.objects.get(id=student_id)
        try:
            status_list = StudentStatus.objects.all()
            flag = True
            for obj in status_list:
                if obj.student_id == student:
                    flag = False
            if flag:
                status = StudentStatus(student_id=student, status=student_status)
                status.save()
                messages.success(request, "Student Status configured Successfully!")
                return redirect("set_student_status")
            else:
                messages.success(request, "Student Status already configured!")
                return redirect('set_student_status')
        except:
            messages.error(request, "Failed to configure Student Status !")
            return redirect("set_student_status")


def manage_student_status(request):
    student_status = StudentStatus.objects.all()
    context = {
        "student_status": student_status
    }
    return render(request, "head_template/manage_student_status.html", context)


def delete_student_status(request, status_id):
    status = StudentStatus.objects.get(id=status_id)
    try:
        status.delete()
        messages.success(request, "Status Deleted Successfully.")
        return redirect('manage_student_status')
    except:
        messages.error(request, "Failed to Delete Student Status.")
        return redirect('manage_student_status')


def add_subject(request):
    head = DepartmentHead.objects.get(admin=request.user.id)
    # courses = Courses.objects.all()
    departments = Departments.objects.all()
    batch_lists = BatchInfo.objects.all()
    batch_name_list_ = []
    for batch_list in batch_lists:
        if batch_list.batch_name not in batch_name_list_:
            batch_name_list_.append(batch_list.batch_name)
    # staffs = Users.objects.filter(user_type='2')
    context = {
        # "courses": courses,
        "head": head,
        "departments": departments,
        "batchinfos": batch_name_list_,
    }
    return render(request, 'head_template/add_subject_template.html', context)


def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('head_add_subject')
    else:
        subject_name = request.POST.get('subject')
        subject_code = request.POST.get('subject_code')
        semester = request.POST.get('semester')
        curricclum = request.POST.get('curricclum')

        # course_id = request.POST.get('course')
        # course = Courses.objects.get(id=course_id)

        department_id = request.POST.get('department')
        department = Departments.objects.get(id=department_id)

        batch = request.POST.get('batch')
        # batch = BatchInfo.objects.get(id=batch_id)

        # staff_id = request.POST.get('staff')
        # staff = Users.objects.get(id=staff_id)
        try:
            subjects_obj = Course.objects.all()
            flag = True
            for obj in subjects_obj:
                if obj.subject_code == subject_code:
                    flag = False
            if flag:
                subject = Course(subject_name=subject_name, subject_code=subject_code,
                                 department_id=department,
                                 batch=int(batch), semester=semester, curicullem=curricclum)
                subject.save()
                messages.success(request, "Subject Added Successfully!")
                return redirect('head_add_subject')
            else:
                messages.success(request, "Subject already added!")
                return redirect('head_add_subject')
        except Exception as e:
            print(f"An error occurred: {e}")
            messages.error(request, "Failed to Add Subject!")
            return redirect('head_add_subject')


def manage_subject(request):
    head = DepartmentHead.objects.get(admin=request.user.id)
    subjects = Course.objects.filter(department_id=head.department_id)
    context = {
        "subjects": subjects
    }
    return render(request, 'head_template/manage_subject_template.html', context)


def edit_subject(request, subject_id):
    subject = Course.objects.get(id=subject_id)
    batch_lists = BatchInfo.objects.all()
    batch_name_list_ = []
    for batch_list in batch_lists:
        if batch_list.batch_name not in batch_name_list_:
            batch_name_list_.append(batch_list.batch_name)
    departments = Departments.objects.all()
    # courses = Courses.objects.all()
    # staffs = Users.objects.filter(user_type='2')
    context = {
        "subject": subject,
        # "courses": courses,
        "departments": departments,
        "batchinfos": batch_name_list_,
        # "staffs": staffs,
        "id": subject_id
    }
    return render(request, 'head_template/edit_subject_template.html', context)


def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject')
        subject_code = request.POST.get('subject_code')
        semester = request.POST.get('semester')
        curicullem = request.POST.get('curricclum')
        # course_id = request.POST.get('course')
        department_id = request.POST.get('department')
        batch = request.POST.get('batch')
        # staff_id = request.POST.get('staff')

        # try:
        subject = Course.objects.get(id=subject_id)
        subject.subject_name = subject_name
        subject.subject_code = subject_code
        subject.semester = semester
        subject.curicullem = curicullem
        #
        # course = Courses.objects.get(id=course_id)
        # subject.course_id = course

        department = Departments.objects.get(id=department_id)
        subject.department_id = department

        # batchinfo = BatchInfo.objects.get(id=batch_id)
        subject.batch = batch

        # staff = Users.objects.get(id=staff_id)
        # subject.staff_id = staff

        subject.save()

        messages.success(request, "Subject Updated Successfully.")
        # return redirect('/edit_subject/'+subject_id)
        return HttpResponseRedirect(reverse("head_edit_subject", kwargs={"subject_id": subject_id}))

        # except:
        messages.error(request, "Failed to Update Subject.")
        return HttpResponseRedirect(reverse("head_edit_subject", kwargs={"subject_id": subject_id}))
        # return redirect('/edit_subject/'+subject_id)


def delete_subject(request, subject_id):
    subject = Course.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('head_manage_subject')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('head_manage_subject')


def assign_instructor(request):
    try:
        # Get the department head
        head = DepartmentHead.objects.get(admin=request.user.id)
        
        # Get unique batch names from Course model (since Course has batch field)
        # OR from RegisterForCourse if that's where subjects are registered
        batchinfos = Course.objects.filter(
            department_id=head.department_id
        ).values_list('batch', flat=True).distinct()
        
        # If you want from RegisterForCourse:
        # batchinfos = RegisterForCourse.objects.filter(
        #     department_id=head.department_id
        # ).values_list('batch', flat=True).distinct()
        
        # Get unique sections from RegisterForCourse
        sections = RegisterForCourse.objects.filter(
            department_id=head.department_id
        ).values_list('section', flat=True).distinct()
        
        # Get instructors for this department
        instructors = Instructor.objects.filter(department_id=head.department_id)
        
        context = {
            'batchinfos': sorted(batchinfos),
            'sections': sorted(sections),
            'staffs': instructors,
        }
        return render(request, 'head_template/assign_instructor_template.html', context)
        
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('head_home')


def assign_instructor_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid request method!")
        return redirect('assign_instructor')
    
    try:
        # Get form data
        subject_id = request.POST.get('subject_id')
        staff_id = request.POST.get('staff_id')  # Changed from 'staff'
        batch = request.POST.get('batch')
        section = request.POST.get('section')
        class_type = request.POST.get('class_type')
        
        print(f"DEBUG: Form data - subject_id={subject_id}, staff_id={staff_id}, "
              f"batch={batch}, section={section}, class_type={class_type}")
        
        # Validate required fields
        if not all([subject_id, staff_id, batch, section, class_type]):
            messages.error(request, "All fields are required!")
            return redirect('assign_instructor')
        
        # Get department head for department_id
        head = DepartmentHead.objects.get(admin=request.user.id)
        
        # Get Course
        try:
            subject = Course.objects.get(id=subject_id)
            print(f"DEBUG: Found course: {subject.subject_name}")
        except Course.DoesNotExist:
            messages.error(request, f"Course with ID {subject_id} does not exist!")
            return redirect('assign_instructor')
        
        # Get Instructor (not Staffs)
        try:
            instructor = Instructor.objects.get(id=staff_id)
            print(f"DEBUG: Found instructor: {instructor.admin.first_name}")
        except Instructor.DoesNotExist:
            messages.error(request, f"Instructor with ID {staff_id} does not exist!")
            return redirect('assign_instructor')
        
        # Convert batch to integer for AssignInstructor model
        try:
            batch_int = int(batch)
        except ValueError:
            messages.error(request, "Invalid batch format!")
            return redirect('assign_instructor')
        
        # Check if assignment already exists
        existing_assignment = AssignInstructor.objects.filter(
            batch=batch_int,
            section=section,
            subject_id=subject,
            department_id=head.department_id,
            class_type=class_type
        ).first()
        
        if existing_assignment:
            messages.warning(request, f"This assignment already exists! Instructor: {existing_assignment.staff_id.admin.get_full_name()}")
            return redirect('assign_instructor')
        
        # Create new assignment
        assignment = AssignInstructor(
            batch=batch_int,
            section=section,
            subject_id=subject,
            department_id=head.department_id,
            class_type=class_type,
            staff_id=instructor
        )
        assignment.save()
        
        messages.success(request, f"Instructor {instructor.admin.get_full_name()} assigned to {subject.subject_name} successfully!")
        return redirect('assign_instructor')
        
    except DepartmentHead.DoesNotExist:
        messages.error(request, "Department head not found!")
        return redirect('assign_instructor')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('assign_instructor')
    
    
    


def manage_assign_instructor(request):
    head = DepartmentHead.objects.get(admin=request.user.id)
    assignInstructors = AssignInstructor.objects.filter(department_id=head.department_id)
    context = {
        "assignInstructors": assignInstructors
    }
    return render(request, 'head_template/manage_assign_instructor_template.html', context)


def assign_instructor(request):
    head = DepartmentHead.objects.get(admin=request.user.id)

    # Get all subjects in the department
    subjects = Course.objects.filter(department_id=head.department_id)

    # Get unique batch years and sections for dropdowns
    batch_list = BatchInfo.objects.values_list('batch_name', flat=True).distinct().order_by('batch_name')
    section_list = BatchInfo.objects.values_list('section', flat=True).distinct().order_by('section')

    # Get all instructors in the department
    staffs = Instructor.objects.filter(department_id=head.department_id)

    context = {
        "subjects": subjects,
        "staffs": staffs,
        "batchinfos": batch_list,
        "sections": section_list,
    }
    return render(request, 'head_template/assign_instructor_template.html', context)



def edit_assign_instructor(request, assign_id):
    """
    Edit an existing instructor assignment.
    """
    try:
        assign_instructor = AssignInstructor.objects.get(id=assign_id)
        # ... rest of your code ...
        context = {
            # ... other context ...
            'assign_instructor': assign_instructor,  # IMPORTANT: This name must match template
        }
        return render(request, 'head_template/edit_assign_instructor_template.html', context)
        
    except AssignInstructor.DoesNotExist:
        messages.error(request, "Assignment not found!")
        return redirect('manage_assign_instructor')
    except DepartmentHead.DoesNotExist:
        messages.error(request, "Department head not found!")
        return redirect('manage_assign_instructor')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('manage_assign_instructor')



def edit_assign_instructor_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid request method!")
        return redirect('manage_assign_instructor')
    
    try:
        # Get form data
        assign_instructor_id = request.POST.get('assign_instructor_id')
        subject_id = request.POST.get('subject_id')
        staff_id = request.POST.get('staff_id')
        batch = request.POST.get('batch')
        section = request.POST.get('section')
        class_type = request.POST.get('class_type')
        
        print(f"DEBUG EDIT SAVE: assign_id={assign_instructor_id}, subject_id={subject_id}, "
              f"staff_id={staff_id}, batch={batch}, section={section}, class_type={class_type}")
        
        # Validate required fields
        if not assign_instructor_id:
            messages.error(request, "Assignment ID is required!")
            return redirect('manage_assign_instructor')
        
        if not all([subject_id, staff_id, batch, section, class_type]):
            messages.error(request, "All fields are required!")
            return redirect('manage_assign_instructor')
        
        # Get the assignment
        assign_instructor = AssignInstructor.objects.get(id=int(assign_instructor_id))
        
        # Update fields
        assign_instructor.batch = int(batch)
        assign_instructor.section = section
        assign_instructor.subject_id = Course.objects.get(id=subject_id)
        assign_instructor.staff_id = Instructor.objects.get(id=staff_id)
        assign_instructor.class_type = class_type
        assign_instructor.save()
        
        messages.success(request, "Assignment updated successfully!")
        return redirect('manage_assign_instructor')
        
    except AssignInstructor.DoesNotExist:
        messages.error(request, "Assignment not found!")
        return redirect('manage_assign_instructor')
    except Course.DoesNotExist:
        messages.error(request, "Course not found!")
        return redirect('edit_assign_instructor', assign_id=assign_instructor_id)
    except Instructor.DoesNotExist:
        messages.error(request, "Instructor not found!")
        return redirect('edit_assign_instructor', assign_id=assign_instructor_id)
    except ValueError:
        messages.error(request, "Invalid assignment ID!")
        return redirect('manage_assign_instructor')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        # Try to redirect back to edit page
        if assign_instructor_id:
            return redirect('edit_assign_instructor', assign_id=assign_instructor_id)
        else:
            return redirect('manage_assign_instructor')


def delete_assign_instructor(request, assign_instructor_id):
    assignInstructor = AssignInstructor.objects.get(id=assign_instructor_id)
    try:
        assignInstructor.delete()
        messages.success(request, "assignInstructor Deleted Successfully.")
        return redirect('manage_assign_instructor')
    except:
        messages.error(request, "Failed to Delete assignInstructor.")
        return redirect('manage_assign_instructor')
    
@csrf_exempt
def load_subjects_section_batch(request):
    if request.method == "POST":
        print("POST DATA:", request.POST)

        batch_id = request.POST.get('batch')
        section_id = request.POST.get('section')
        print("Batch:", batch_id, "Section:", section_id)

        if not batch_id or not section_id:
            print("Batch or Section is missing!")
            return JsonResponse([], safe=False)

        try:
            head = DepartmentHead.objects.get(admin=request.user.id)
        except DepartmentHead.DoesNotExist:
            print("DepartmentHead not found for user:", request.user.id)
            return JsonResponse([], safe=False)

        try:
            subjects_qs = RegisterForCourse.objects.filter(
                batch=batch_id,
                section=section_id,
                department_id=head.department_id
            ).select_related('subject_id')
        except Exception as e:
            print("Query Error:", e)
            return JsonResponse([], safe=False)

        list_data = []
        subject_ids = set()
        for obj in subjects_qs:
            if obj.subject_id.id not in subject_ids:
                list_data.append({
                    "id": obj.subject_id.id,
                    "name": obj.subject_id.subject_name
                })
                subject_ids.add(obj.subject_id.id)

        print("Subjects Data:", list_data)
        return JsonResponse(list_data, safe=False)

    return JsonResponse([], safe=False)




    


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = Users.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def student_feedback_message(request):
    head_id = request.user.id
    # head_orginal_id = Head.objects.get(admin=head_id)
    # students = Students.objects.filter(department_id=head_orginal_id.department_id)
    # feedback_list = []
    # flag = True
    # feedbacks = FeedBackStudent.objects.all()
    #
    # for feedback in feedbacks:
    #     if feedback.student_id in students:
    #         feedback_list.append(feedback)
    feedbacks = FeedBackStudent.objects.filter(receiver=head_id)
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'head_template/student_feedback_template.html', context)


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
    head_id = request.user.id
    head_orginal_id = DepartmentHead.objects.get(admin=head_id)
    staffs = Instructor.objects.filter(department_id=head_orginal_id.department_id)
    feedback_list = []
    feedbacks = FeedBackStaffs.objects.all()
    for feedback in feedbacks:
        if feedback.staff_id in staffs:
            feedback_list.append(feedback)

    context = {
        "feedbacks": feedback_list
    }
    return render(request, 'head_template/staff_feedback_template.html', context)


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


def staff_leave_view(request):
    head_id = request.user.id
    head_orginal_id = DepartmentHead.objects.get(admin=head_id)
    staffs = Instructor.objects.filter(department_id=head_orginal_id.department_id)
    leave_list = []
    leaves = LeaveReportStaff.objects.all()
    for leave in leaves:
        if leave.staff_id in staffs:
            leave_list.append(leave)

    context = {
        "leaves": leave_list
    }
    return render(request, 'head_template/staff_leave_view.html', context)


def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('head_staff_leave_view')


def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('head_staff_leave_view')


def head_manage_attendance(request):
    head = DepartmentHead.objects.get(admin=request.user.id)
    attendance_fr = Attendance.objects.filter(department_id=head.department_id)
    context = {
        "attendance_fr": attendance_fr,
    }
    return render(request, 'head_template/delete_attendance_template.html', context)


def head_delete_attendance(request, attendance_id):
    attendance_fr = Attendance.objects.get(id=attendance_id)
    try:
        attendance_fr.delete()
        messages.success(request, "The Recoded Attendance is Deleted Successfully!")
        return redirect('head_manage_attendance')
    except:
        messages.error(request, "Failed to Delete the Recoded Attendance!")
        return redirect('head_manage_attendance')


def head_view_attendance(request):
    head = DepartmentHead.objects.get(admin=request.user.id)
    # subjects = Course.objects.filter(department_id=head.department_id)
    sub_list = Attendance.objects.filter(department_id=head.department_id)
    subjects = []
    # department_list = []
    sections = []
    batch_list = []
    for sub in sub_list:
        if sub.subject_id not in subjects:
            subjects.append(sub.subject_id)
        if sub.section not in sections:
            sections.append(sub.section)
        if sub.batch not in batch_list:
            batch_list.append(sub.batch)

    # register_for_courses = []
    # for subject in subjects:
    #     register_for_course = RegisterForCourse.objects.filter(subject_id=subject.id)
    #     register_for_courses.append(register_for_course)
    #
    # section_list = []
    # section_check_list = []
    # for register_for_course in register_for_courses:
    #     for register_forcourse in register_for_course:
    #         section = BatchInfo.objects.filter(id=register_forcourse.section.id)
    #         for sec in section:
    #             if sec.section not in section_check_list:
    #                 section_check_list.append(sec.section)
    #                 section_list.append(section)

    attendance_list = []
    for attendance in sub_list:
        if attendance.attendance_type not in attendance_list:
            attendance_list.append(attendance.attendance_type)

    context = {
        "attendances": attendance_list,
        "subjects": subjects,
        "sections": sections,
        "batches": batch_list,
    }
    return render(request, "head_template/head_view_attendance.html", context)


def head_view_attendance_final(request):
    head = DepartmentHead.objects.get(admin=request.user.id)
    # subjects = Course.objects.filter(department_id=head.department_id)
    sub_list = Attendance.objects.filter(department_id=head.department_id)
    subjects = []
    # department_list = []
    sections = []
    batch_list = []
    for sub in sub_list:
        if sub.subject_id not in subjects:
            subjects.append(sub.subject_id)
        if sub.section not in sections:
            sections.append(sub.section)
        if sub.batch not in batch_list:
            batch_list.append(sub.batch)

    # register_for_courses = []
    # for subject in subjects:
    #     register_for_course = RegisterForCourse.objects.filter(subject_id=subject.id)
    #     register_for_courses.append(register_for_course)
    #
    # section_list = []
    # section_check_list = []
    # for register_for_course in register_for_courses:
    #     for register_forcourse in register_for_course:
    #         section = BatchInfo.objects.filter(id=register_forcourse.section.id)
    #         for sec in section:
    #             if sec.section not in section_check_list:
    #                 section_check_list.append(sec.section)
    #                 section_list.append(section)

    attendance_list = []
    for attendance in sub_list:
        if attendance.attendance_type not in attendance_list:
            attendance_list.append(attendance.attendance_type)

    context = {
        "attendances": attendance_list,
        "subjects": subjects,
        "sections": sections,
        "batches": batch_list,
    }
    return render(request, "head_template/head_view_attendance_final.html", context)


@csrf_exempt
def head_get_attendance_dates(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    head = DepartmentHead.objects.get(admin=request.user.id)
    section = request.POST.get("section")
    batch = request.POST.get("batch")
    attendance_type = request.POST.get("attendance_type")
    # session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Course
    # Getting all data from subject model based on subject_id
    subject_model = Course.objects.get(id=subject_id)
    department_model = Departments.objects.get(id=head.department_id.id)
    # section_model = BatchInfo.objects.get(id=section_id)

    # session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(subject_id=subject_model, department_id=department_model,
                                           section=section,
                                           batch=batch, attendance_type=attendance_type)

    attendance_list = AttendanceReport.objects.all()
    student_list = []
    count = 0
    for attendance_obj in attendance_list:
        if attendance_obj.attendance_id:
            if attendance_obj.student_id not in student_list:
                student_list.append(attendance_obj.student_id)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date)}
        # "session_year_id": attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def head_get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []
    status_list = StudentStatus.objects.all()
    students_list = []
    for status in status_list:
        students_list.append(status.student_id)

    for student in attendance_data:
        if student.student_id not in students_list:
            data_small = {"id": student.student_id.student_id,
                          "name": student.student_id.admin.first_name + " " + student.student_id.admin.last_name,
                          "status": student.status}
            list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def head_get_student_final(request):
    # Getting Values from Ajax POST 'Fetch Student'
    section = request.POST.get('section')
    batch = request.POST.get('batch')
    subject_id = request.POST.get('subject')
    attendance_type = request.POST.get('attendance_type')
    subject = Course.objects.get(id=subject_id)
    head = DepartmentHead.objects.get(admin=request.user.id)

    attendance_lecture = Attendance.objects.filter(section=section, batch=batch, subject_id=subject,
                                                   department_id=head.department_id, attendance_type='lecture')
    attendance_lab = Attendance.objects.filter(section=section, batch=batch, subject_id=subject,
                                               department_id=head.department_id, attendance_type='lab_class')
    total_lecture_attendance = attendance_lecture.count()
    total_lab_attendance = attendance_lab.count()

    total_attendance_lecture = AttendanceReport.objects.filter(attendance_id__in=attendance_lecture)
    total_attendance_lab = AttendanceReport.objects.filter(attendance_id__in=attendance_lab)

    attendance_all = Attendance.objects.filter(section=section, batch=batch, subject_id=subject,
                                               department_id=head.department_id)
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

    attendance_weight = AttendanceWeight.objects.filter(department_id=head.department_id, batch=batch,
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
    if attendance_type == 'non_final':
        for student in total_final_not_taker_list:
            if student not in students_list and student not in students:
                data_small = {"id": student.student_id,
                              "name": student.admin.first_name + " " + student.admin.last_name}
                list_data.append(data_small)
                students.append(student)
    if attendance_type == 'final':
        for student in final_taking_student_list:
            if student not in students_list:
                data_small = {"id": student.student_id,
                              "name": student.admin.first_name + " " + student.admin.last_name}
                list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


# Dependent Dropdown List
@csrf_exempt
def load_subjects(request):
    if request.method == "POST":
        head = DepartmentHead.objects.get(admin=request.user.id)
        curricclum = request.POST['curricclum']
        semester = request.POST['semester']
        batch = request.POST['batch']
        # batch_obj = BatchInfo.objects.filter(batch_name=batch)
        # try:
        subjects = Course.objects.filter(department_id=head.department_id, batch=batch, curicullem=curricclum,
                                         semester=semester)
        list_data = []
        for subject in subjects:
            data_small = {"id": subject.id,
                          "name": subject.subject_name,
                          }
            list_data.append(data_small)
        # except Exception:
        # data['error_message'] = 'error'
        # return JsonResponse(data)
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def load_subjects_batch(request):
    if request.method == "POST":
        batch = request.POST['batch']
        head = DepartmentHead.objects.get(admin=request.user.id)
        subjects = Course.objects.filter(batch=batch, department_id=head.department_id)
        weights = AttendanceWeight.objects.all()
        subject_list = []
        for weight in weights:
            subject_list.append(weight.subject_id)

        list_data = []
        for subject in subjects:
            if subject not in subject_list:
                data_small = {"id": subject.id,
                              "name": subject.subject_name,
                              }
                list_data.append(data_small)
        # except Exception:
        # data['error_message'] = 'error'
        # return JsonResponse(data)
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def load_sections_batch(request):
    if request.method == "POST":
        batch_id = request.POST['batch']
        batch = BatchInfo.objects.get(id=batch_id)
        # semester = request.POST['semester']
        # try:
        sections = RegisterForCourse.objects.filter(batch=batch.batch_name)
        list_data = []
        for section in sections:
            data_small = {"id": section.section.section,
                          "name": section.section.section,
                          }
            list_data.append(data_small)
        # except Exception:
        # data['error_message'] = 'error'
        # return JsonResponse(data)
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def load_subjects_section_batch(request):
    if request.method == "POST":
        try:
            # Debug logging
            print(f"DEBUG: Received POST data: {dict(request.POST)}")
            
            head = DepartmentHead.objects.get(admin=request.user.id)
            batch = request.POST.get('batch')
            section = request.POST.get('section')
            
            print(f"DEBUG: Batch={batch}, Section={section}, Department={head.department_id.id}")
            
            if not batch or not section:
                return JsonResponse({'error': 'Batch and section are required'}, status=400)
            
            # Convert batch to string since RegisterForCourse.batch is CharField
            batch_str = str(batch)
            
            # Get subjects from RegisterForCourse
            # Remove .distinct('subject_id') since SQLite doesn't support it
            register_records = RegisterForCourse.objects.filter(
                batch=batch_str,  # Convert to string
                section=section,
                department_id=head.department_id
            ).select_related('subject_id')
            
            print(f"DEBUG: Found {register_records.count()} register records")
            
            list_data = []
            subject_ids = []
            
            # Manual distinct using Python
            for record in register_records:
                subject = record.subject_id
                if subject.id not in subject_ids:
                    data_small = {
                        "id": subject.id,
                        "name": f"{subject.subject_code} - {subject.subject_name}",
                    }
                    list_data.append(data_small)
                    subject_ids.append(subject.id)
            
            print(f"DEBUG: Returning {len(list_data)} distinct subjects")
            return JsonResponse(list_data, safe=False)
            
        except DepartmentHead.DoesNotExist:
            return JsonResponse({'error': 'Department head not found'}, status=400)
        except Exception as e:
            print(f"DEBUG: Error in load_subjects_section_batch: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)



def head_profile(request):
    head = DepartmentHead.objects.get(admin=request.user.id)
    user = Users.objects.get(id=head.staff_id.admin.id)
    context = {
        "head": head,
        "user": user
    }
    return render(request, 'head_template/head_profile.html', context)


def head_profile_pic(request):
    head = DepartmentHead.objects.get(admin=request.user.id)
    img_path = head.staff_id.profile_pic
    return HttpResponse(img_path)


def head_profile_update(request):
    if request.method != "POST" and request.FILES['profile']:
        messages.error(request, "Invalid Method!")
        return redirect('head_profile')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        try:
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None
            head = DepartmentHead.objects.get(admin=request.user.id)
            head.admin.username = username
            head.staff_id.admin.first_name = first_name
            head.staff_id.admin.last_name = last_name
            head.staff_id.admin.email = email
            head.staff_id.profile_pic = profile_pic_url
            if password != None and password != "":
                head.admin.set_password(password)
            head.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('head_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('head_profile')


def staff_profile(request):
    pass


def student_profile(requtest):
    pass
