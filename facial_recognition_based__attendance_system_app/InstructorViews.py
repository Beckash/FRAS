from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from .FacialRecognition.mainOrginal import MainClass
import cv2
from mtcnn.mtcnn import MTCNN
from .models import Users, Instructor, Course, Students, SessionYearModel, \
    Attendance, \
    AttendanceReport, LeaveReportStaff, FeedBackStaffs, RegisterForCourse, \
    Departments, BatchInfo, FeedBackStudent, LeaveReportStudent, ICT_Professional, \
    DepartmentHead, AssignInstructor, StudentStatus, AttendanceWeight, Camera

from datetime import datetime
import time


def staff_home(request):
    # Fetching All Students under Staff

    staff_id = Instructor.objects.get(admin=request.user.id)
    assignInstructor = AssignInstructor.objects.filter(staff_id=staff_id)
    subjects = []
    for assign in assignInstructor:
        subjects.append(Course.objects.get(id=assign.subject_id.id))

    # course_id_list = []
    students = []
    # for subject in subjects:
    #     course = Courses.objects.get(id=subject.course_id.id)
    #     course_id_list.append(course.id)

    for subject in subjects:
        objs = RegisterForCourse.objects.filter(subject_id=subject)
        for obj in objs:
            if obj.student_id not in students:
                students.append(obj.student_id)

    # final_course = []
    # Removing Duplicate Course Id
    # for course_id in course_id_list:
    #     if course_id not in final_course:
    #         final_course.append(course_id)

    # students_count = Students.objects.filter(course_id__in=final_course).count()
    students_count = len(students)
    subject_count = len(subjects)

    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
    # Fetch All Approve Leave
    # staff = Instructor.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(staff_id=staff_id, leave_status=1).count()

    # Fetch Attendance Data by Course
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    # students_attendance = Students.objects.filter(course_id__in=final_course)
    students_attendance = students
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    subject_list = []
    flag = True
    for student in students_attendance:
        attendance = AttendanceReport.objects.filter(student_id=student.id)
        for a in attendance:
            if flag:
                flag = False
                subject_list.append(a.attendance_id.subject_id.subject_name)

        attendance_present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
        student_list.append(student.admin.first_name + " " + student.admin.last_name)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)
        flag = True

    context = {
        "students_count": students_count,
        "attendance_count": attendance_count,
        "leave_count": leave_count,
        "subject_count": subject_count,
        "subject_list": subject_list,
        "attendance_list": attendance_list,
        "subject_list": subject_list,
        "student_list": student_list,
        "attendance_present_list": student_list_attendance_present,
        "attendance_absent_list": student_list_attendance_absent
    }
    return render(request, "instructor_templates/staff_home_template.html", context)


# Camera Views
def add_camera(request):
    staff_id = Instructor.objects.get(admin=request.user.id)
    sub_list = AssignInstructor.objects.filter(staff_id=staff_id)
    subjects = []
    for sub in sub_list:
        if sub.subject_id not in subjects:
            subjects.append(sub.subject_id)

    # subjects = Course.objects.filter(staff_id=request.user.id)
    department_list = []
    register_for_courses = []
    for subject in subjects:
        departments = Departments.objects.get(id=subject.department_id.id)
        register_for_course = RegisterForCourse.objects.filter(subject_id=subject.id)
        # if departments not in department_list:
        department_list.append(departments)
        register_for_courses.append(register_for_course)
    departments = []
    for department in department_list:
        if department not in departments:
            departments.append(department)
    section_list = []
    batch_list = []
    for register_for_course in register_for_courses:
        for register_forcourse in register_for_course:
            if register_forcourse.section not in section_list:
                section_list.append(register_forcourse.section)
            if register_forcourse.batch not in batch_list:
                batch_list.append(register_forcourse.batch)
    context = {
        "departments": departments,
        "sections": section_list,
        "batches": batch_list,
    }
    return render(request, "instructor_templates/add_camera_template.html", context)


def add_camera_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_camera')
    else:
        department_id = request.POST.get('department')
        section = request.POST.get('section')
        batch = request.POST.get('batch')
        camera_direction = request.POST.get('direction')
        ip_address = request.POST.get('ip_address')

        try:
            department = Departments.objects.get(id=department_id)
            camera = Camera.objects.all()
            flag = True
            for obj in camera:
                if obj.direction == camera_direction and obj.ip_address == ip_address:
                    flag = False
            if flag:
                camera_model = Camera(direction=camera_direction, ip_address=ip_address,
                                      department_id=department, section=section, batch=batch)
                camera_model.save()
                messages.success(request, "Camera Added Successfully!")
                return redirect('add_camera')
            else:
                messages.success(request, "Camera Already Existed!")
                return redirect('add_camera')
        except:
            messages.error(request, "Failed to Add Camera!")
            return redirect('add_camera')


def manage_camera(request):
    camera = Camera.objects.all()
    context = {
        "cameras": camera
    }
    return render(request, 'instructor_templates/manage_camera_template.html', context)


def edit_camera(request, camera_id):
    camera = Camera.objects.get(id=camera_id)
    context = {
        "camera": camera,
        "id": camera_id
    }
    return render(request, 'instructor_templates/edit_camera_template.html', context)


def edit_camera_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        camera_id = request.POST.get('camera_id')
        camera_direction = request.POST.get('direction')
        ip_address = request.POST.get('ip_address')

        try:
            camera = Camera.objects.get(id=camera_id)
            camera.direction = camera_direction
            camera.ip_address = ip_address
            camera.save()

            messages.success(request, "Camera Information Updated Successfully.")
            return redirect('/staff_edit_camera/' + camera_id)

        except:
            messages.error(request, "Failed to Update Camera Information.")
            return redirect('/staff_edit_camera/' + camera_id)


def delete_camera(request, camera_id):
    camera = Camera.objects.get(id=camera_id)
    try:
        camera.delete()
        messages.success(request, "Camera Information Deleted Successfully.")
        return redirect('manage_camera')
    except:
        messages.error(request, "Failed to Delete Camera.")
        return redirect('manage_camera')


def staff_take_attendance(request):
    # subjects = Course.objects.filter(staff_id=request.user.id)
    # session_years = SessionYearModel.objects.all()
    # context = {
    #     "subjects": subjects,
    #     "session_years": session_years
    # }
    staff_id = Instructor.objects.get(admin=request.user.id)
    sub_list = AssignInstructor.objects.filter(staff_id=staff_id)
    subjects = []
    for sub in sub_list:
        if sub.subject_id not in subjects:
            subjects.append(sub.subject_id)

    # subjects = Course.objects.filter(staff_id=request.user.id)
    department_list = []
    register_for_courses = []
    for subject in subjects:
        departments = Departments.objects.get(id=subject.department_id.id)
        register_for_course = RegisterForCourse.objects.filter(subject_id=subject.id)
        # if departments not in department_list:
        department_list.append(departments)
        register_for_courses.append(register_for_course)
    departments = []
    for department in department_list:
        if department not in departments:
            departments.append(department)
    section_list = []
    batch_list = []
    for register_for_course in register_for_courses:
        for register_forcourse in register_for_course:
            if register_forcourse.section not in section_list:
                section_list.append(register_forcourse.section)
            if register_forcourse.batch not in batch_list:
                batch_list.append(register_forcourse.batch)

    # session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "departments": departments,
        "sections": section_list,
        "batches": batch_list,
    }

    return render(request, "instructor_templates/take_attendance_template_correct.html", context)


def staff_view_attendance_final(request):
    # subjects = Course.objects.filter(staff_id=request.user.id)
    # session_years = SessionYearModel.objects.all()
    # context = {
    #     "subjects": subjects,
    #     "session_years": session_years
    # }
    staff_id = Instructor.objects.get(admin=request.user.id)
    sub_list = AssignInstructor.objects.filter(staff_id=staff_id)
    subjects = []
    for sub in sub_list:
        if sub.subject_id not in subjects:
            subjects.append(sub.subject_id)

    # subjects = Course.objects.filter(staff_id=request.user.id)
    department_list = []
    register_for_courses = []
    for subject in subjects:
        departments = Departments.objects.get(id=subject.department_id.id)
        register_for_course = RegisterForCourse.objects.filter(subject_id=subject.id)
        # if departments not in department_list:
        department_list.append(departments)
        register_for_courses.append(register_for_course)
    departments = []
    for department in department_list:
        if department not in departments:
            departments.append(department)
    section_list = []
    batch_list = []
    for register_for_course in register_for_courses:
        for register_forcourse in register_for_course:
            if register_forcourse.section not in section_list:
                section_list.append(register_forcourse.section)
            if register_forcourse.batch not in batch_list:
                batch_list.append(register_forcourse.batch)

    # session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "departments": departments,
        "sections": section_list,
        "batches": batch_list,
    }

    return render(request, "instructor_templates/staff_view_attendance_final.html", context)


def fr_take_attendance(request):
    staff_id = Instructor.objects.get(admin=request.user.id)
    sub_list = AssignInstructor.objects.filter(staff_id=staff_id)
    subjects = []
    for sub in sub_list:
        if sub.subject_id not in subjects:
            subjects.append(sub.subject_id)

    # subjects = Course.objects.filter(staff_id=request.user.id)
    department_list = []
    register_for_courses = []
    for subject in subjects:
        departments = Departments.objects.get(id=subject.department_id.id)
        register_for_course = RegisterForCourse.objects.filter(subject_id=subject.id)
        # if departments not in department_list:
        department_list.append(departments)
        register_for_courses.append(register_for_course)
    departments = []
    for department in department_list:
        if department not in departments:
            departments.append(department)
    section_list = []
    batch_list = []
    for register_for_course in register_for_courses:
        for register_forcourse in register_for_course:
            if register_forcourse.section not in section_list:
                section_list.append(register_forcourse.section)
            if register_forcourse.batch not in batch_list:
                batch_list.append(register_forcourse.batch)

    # session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "departments": departments,
        "batches": batch_list,
        "sections": section_list,
        # "session_years": session_years
    }
    return render(request, "instructor_templates/fr_take_attendance_template.html", context)


def fr_take_attendance_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('fr_take_attendance')
    else:
        staff = Instructor.objects.get(admin=request.user.id)
        ip_address = request.POST.get('ip')
        subject_id = request.POST.get('subject')
        subject = Course.objects.get(id=subject_id)
        department_id = request.POST.get('department')
        department = Departments.objects.get(id=department_id)
        attendance_type = request.POST.get('attendance_type')
        batch = request.POST.get('batch')
        section = request.POST.get('section')
        # sections = BatchInfo.objects.get(id=section)
        attendance_date = request.POST.get('attendance_date')
        try:
            attendance_fr = Attendance(subject_id=subject, department_id=department, attendance_type=attendance_type,
                                       section=section, batch=batch, attendance_date=attendance_date, staff_id=staff)
            attendance_fr.save()
            live_attendance(request, ip_address=ip_address, attendance_fr=attendance_fr)
            return redirect('fr_take_attendance')
        except:
            return redirect('fr_take_attendance')


def live_attendance(request, ip_address, attendance_fr):
    detector = MTCNN()
    url = ip_address + '/video'
    cap = cv2.VideoCapture(url)
    # cap = cv2.VideoCapture(0)

    student_list = []
    # previous_time = int(round(time.time() * 1000))
    while True:
        # Capture frame-by-frame
        __, frame = cap.read()

        # Use MTCNN to detect faces
        result = detector.detect_faces(frame)
        if result != []:
            for person in result:
                bounding_box = person['box']
                keypoints = person['keypoints']

                cv2.rectangle(frame,
                              (bounding_box[0], bounding_box[1]),
                              (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                              (0, 155, 255),
                              2)

                cv2.circle(frame, (keypoints['left_eye']), 2, (0, 155, 255), 2)
                cv2.circle(frame, (keypoints['right_eye']), 2, (0, 155, 255), 2)
                cv2.circle(frame, (keypoints['nose']), 2, (0, 155, 255), 2)
                cv2.circle(frame, (keypoints['mouth_left']), 2, (0, 155, 255), 2)
                cv2.circle(frame, (keypoints['mouth_right']), 2, (0, 155, 255), 2)
            result = MainClass.make_predication(frame)
            continue_flag = True
            try:
                # current_time_in_millisecond = int(round(time.time()*1000))
                # check_time_in_millisecond = previous_time + (10*60*1000)
                # if current_time_in_millisecond > check_time_in_millisecond:
                status_list = StudentStatus.objects.all()
                students_list = []
                for status in status_list:
                    students_list.append(status.student_id)

                student = Students.objects.get(student_id=result)
                if student not in students_list:
                    if student not in student_list:
                        attendance_report_fr = AttendanceReport(student_id=student, attendance_id=attendance_fr,
                                                                status=True)
                        attendance_report_fr.save()
                        student_list.append(student)
            except:
                continue_flag = True
        # display resulting frame
        cv2.imshow('Attendance_Tracking_Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    try:
        # When everything's done, release capture
        cap.release()
        cv2.destroyAllWindows()
        students = RegisterForCourse.objects.filter(section=attendance_fr.section, subject_id=attendance_fr.subject_id,
                                                    department_id=attendance_fr.department_id)
        for student in students:
            if student.student_id not in student_list:
                attendance_report_fr = AttendanceReport(student_id=student.student_id, attendance_id=attendance_fr,
                                                        status=False)
                attendance_report_fr.save()

        messages.success(request, "Attendance  Added Successfully!")
        return redirect('fr_take_attendance')
    except:
        messages.error(request, "Failed to track the Attendance!")
        return redirect('fr_take_attendance')


def staff_fr_view_attendance(request):
    attendance_fr = Attendance.objects.all()
    status_list = StudentStatus.objects.all()
    students_list = []
    students = []
    for status in status_list:
        students_list.append(status.student_id)
    attendance_report_fr = AttendanceReport.objects.all()

    for attendance in attendance_report_fr:
        if attendance.student_id not in students_list:
            students.append(attendance.student_id)

    context = {
        "attendance_fr": attendance_fr,
        "attendance_report_fr": attendance_report_fr,
        "students": students,
    }
    return render(request, 'instructor_templates/view_attendance_template.html', context)


def staff_fr_view_attendanceFR(request):
    staff = Instructor.objects.get(admin=request.user.id)
    attendance_fr = Attendance.objects.filter(staff_id=staff)
    # status_list = StudentStatus.objects.all()
    # students_list = []
    # students = []
    # for status in status_list:
    #     students_list.append(status.student_id)
    # attendance_report_fr = AttendanceReport.objects.all()
    #
    # for attendance in attendance_report_fr:
    #     if attendance.student_id not in students_list:
    #         students.append(attendance.student_id)

    context = {
        "attendance_fr": attendance_fr,
        # "attendance_report_fr": attendance_report_fr,
        # "students": students,
    }
    return render(request, 'instructor_templates/view_attendance_main_template.html', context)


def delete_attendance(request, attendance_id):
    # attendance_fr = Attendance.objects.get(id=attendance_id)
    attendance_report_fr = AttendanceReport.objects.filter(id=attendance_id)
    try:
        attendance_report_fr.delete()
        # attendance_fr.delete()
        messages.success(request, "The Recoded Attendance is Deleted Successfully!")
        return redirect('staff_fr_view_attendance')
    except:
        messages.error(request, "Failed to Delete the Recoded Attendance!")
        return redirect('staff_fr_view_attendance')


def delete_attendancefr(request, attendance_id):
    attendance_fr = Attendance.objects.get(id=attendance_id)
    # attendance_report_fr = AttendanceReport.objects.filter(id=attendance_id)
    try:
        attendance_fr.delete()
        # attendance_fr.delete()
        messages.success(request, "The Recoded Attendance is Deleted Successfully!")
        return redirect('staff_fr_view_attendanceFR')
    except:
        messages.error(request, "Failed to Delete the Recoded Attendance!")
        return redirect('staff_fr_view_attendanceFR')


@csrf_exempt
def staff_get_student_final(request):
    # Getting Values from Ajax POST 'Fetch Student'
    section = request.POST.get('section')
    department_id = request.POST.get('department')
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
        check = attendance_count_lab
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


def staff_apply_leave(request):
    staff_obj = Instructor.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, "instructor_templates/staff_apply_leave_template.html", context)


def staff_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff_obj = Instructor.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_message,
                                            leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('staff_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('staff_apply_leave')


def staff_feedback(request):
    staff_obj = Instructor.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaffs.objects.filter(staff_id=staff_obj)
    admin = ICT_Professional.objects.all()
    head = DepartmentHead.objects.get(department_id=staff_obj.department_id)
    context = {
        "feedback_data": feedback_data,
        "admins": admin,
        "head": head
    }
    return render(request, "instructor_templates/staff_feedback_template.html", context)


def staff_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Instructor.objects.get(admin=request.user.id)
        receiver = request.POST.get('receiver')
        receiver_obj = Users.objects.get(id=receiver)
        try:
            add_feedback = FeedBackStaffs(receiver=receiver_obj, staff_id=staff_obj, feedback=feedback,
                                          feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('staff_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('staff_feedback')


def student_feedback_message(request):
    try:
        staff_id = request.user.id
        # subject = Course.objects.get(staff_id=staff_id)
        # registred_students = RegisterForCourse.objects.filter(subject_id=subject)
        # students = Students.objects.all()
        # feedback_list = []
        # student_list = []
        # flag = True
        # for student in registred_students:
        #     #student.student_id in students:
        #     student_list.append(student.student_id)
        #
        # feedbacks = FeedBackStudent.objects.all()
        # for student in feedbacks:
        #     if student.student_id in student_list:
        #         feedback_list.append(student)
        feedbacks = FeedBackStudent.objects.filter(receiver=staff_id)

    except:
        # messages.error(request, "You haven't assigned for subject!")
        return redirect('staff_home')
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'instructor_templates/student_feedback_template.html', context)


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


def student_leave_view(request):
    # try:
    staff_id = request.user.id

    # subject = Course.objects.get(staff_id=staff_id)
    # registred_students = RegisterForCourse.objects.filter(subject_id=subject)
    # students = Students.objects.all()
    # leave_list = []
    # student_list = []
    # flag = True
    # for student in registred_students:
    #     #if student.student_id in students:
    #     student_list.append(student.student_id)
    # leaves = LeaveReportStudent.objects.all()
    # for leave in leaves:
    #     if leave.student_id in student_list:
    #         leave_list.append(leave)
    leaves = LeaveReportStudent.objects.filter(receiver=staff_id)
    # except:
    #     #messages.error(request, "You haven't assigned for subject!")
    #     return redirect('staff_home')
    context = {
        "leaves": leaves
    }
    return render(request, 'instructor_templates/student_leave_view.html', context)


def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_student_leave_view')


def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_student_leave_view')


# WE don't need csrf_token when using Ajax
@csrf_exempt
def get_students(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    department_id = request.POST.get("department")
    section = request.POST.get("section")
    batch = request.POST.get("batch")

    # Students enroll to Course, Course has Course
    # Getting all data from subject model based on subject_id
    subject_model = Course.objects.get(id=subject_id)
    department_model = Departments.objects.get(id=department_id)
    # section = BatchInfo.objects.get(id=section)

    student_list = RegisterForCourse.objects.filter(subject_id=subject_model, department_id=department_model,
                                                    section=section, batch=batch)

    # session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    status_list = StudentStatus.objects.all()
    students_list = []
    for status in status_list:
        students_list.append(status.student_id)
    list_data = []
    students_id = []
    # flag = False
    for student in student_list:
        # if student.student_id not in students_list:
        #     flag = True
        # else:
        #     student_status = StudentStatus.objects.get(student_id=student.student_id)
        #     if student_status.status == 'normal':
        #         flag = True
        # if flag:
        #     if student.student_id.id not in students_id :
        #         data_small = {"id": student.student_id.id,
        #                       "name": student.student_id.student_id + ": " + student.student_id.admin.first_name + " " + student.student_id.admin.last_name}
        #         list_data.append(data_small)
        #         students_id.append(student.student_id.id)
        if student.student_id not in students_list:
            if student.student_id.id not in students_id:
                data_small = {"id": student.student_id.id,
                              "name": student.student_id.student_id + ": " + student.student_id.admin.first_name + " " + student.student_id.admin.last_name}
                list_data.append(data_small)
                students_id.append(student.student_id.id)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_attendance_data(request):
    # Get Values from Staff Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    staff = Instructor.objects.get(admin=request.user.id)
    student_ids = request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    attendance_type = request.POST.get("attendance_type")
    department_id = request.POST.get("department_id")
    section = request.POST.get("section")
    batch = request.POST.get("batch")
    # session_year_id = request.POST.get("session_year_id")

    subject_model = Course.objects.get(id=subject_id)
    department_model = Departments.objects.get(id=department_id)
    # section = BatchInfo.objects.get(id=section)
    # session_year_model = SessionYearModel.objects.get(id=session_year_id)

    json_student = json.loads(student_ids)
    # print(dict_student[0]['id'])

    # print(student_ids)
    try:
        # First Attendance Data is Saved on Attendance Model
        attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date,
                                attendance_type=attendance_type,
                                department_id=department_model, section=section, batch=batch, staff_id=staff)
        attendance.save()

        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(id=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def staff_update_attendance(request):
    staff_id = Instructor.objects.get(admin=request.user.id)
    sub_list = Attendance.objects.filter(staff_id=staff_id)
    # count = sub_list.count()
    subjects = []
    department_list = []
    sections = []
    batch_list = []
    for sub in sub_list:
        if sub.department_id not in department_list:
            department_list.append(sub.department_id)
        if sub.subject_id not in subjects:
            subjects.append(sub.subject_id)
        if sub.section not in sections:
            sections.append(sub.section)
        if sub.batch not in batch_list:
            batch_list.append(sub.batch)

    attendance_list = []
    for attendance in sub_list:
        if attendance.attendance_type not in attendance_list:
            attendance_list.append(attendance.attendance_type)

    # session_years = SessionYearModel.objects.all()
    context = {
        # "count": count,
        "attendances": attendance_list,
        "subjects": subjects,
        "sections": sections,
        "batches": batch_list,
        "departments": department_list,
        # "session_years": session_years
    }
    return render(request, "instructor_templates/update_attendance_template.html", context)


@csrf_exempt
def get_attendance_dates(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    department_id = request.POST.get("department")
    section = request.POST.get("section")
    batch = request.POST.get("batch")
    attendance_type = request.POST.get("attendance_type")
    # session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Course
    # Getting all data from subject model based on subject_id
    subject_model = Course.objects.get(id=subject_id)
    department_model = Departments.objects.get(id=department_id)
    # section_model = BatchInfo.objects.get(id=section_id)

    # session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(subject_id=subject_model, department_id=department_model,
                                           section=section,
                                           batch=batch, attendance_type=attendance_type)

    # Only Passing Student Id and Student Name Only
    list_data = []
    attendance_ids = []
    for attendance_single in attendance:
        if attendance_single.id not in attendance_ids:
            data_small = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date)}
            # "session_year_id": attendance_single.session_year_id.id}
            list_data.append(data_small)
            attendance_ids.append(attendance_single.id)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    status_list = StudentStatus.objects.all()
    students_list = []
    for status in status_list:
        students_list.append(status.student_id)
    list_data = []
    for student in attendance_data:
        if student.student_id not in students_list:
            data_small = {"id": student.student_id.admin.id,
                          "name": student.student_id.admin.first_name + " " + student.student_id.admin.last_name,
                          "status": student.status}
            list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def update_attendance_data(request):
    student_ids = request.POST.get("student_ids")

    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_student = json.loads(student_ids)

    try:

        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(admin=stud['id'])

            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status = stud['status']

            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


@csrf_exempt
def load_ip_address(request):
    # Getting Values from Ajax POST 'Fetch Student'
    department_id = request.POST.get('department')
    section = request.POST.get('section')
    batch = request.POST.get('batch')

    department = Departments.objects.get(id=department_id)
    ip_address_list = Camera.objects.filter(department_id=department, section=section, batch=batch)
    # Only Passing Student Id and Student Name Only
    list_data = []
    # status_list = StudentStatus.objects.all()
    # students_list = []
    # for status in status_list:
    #     students_list.append(status.student_id)
    for ip in ip_address_list:
        # if student.student_id not in students_list:
        data_small = {"id": ip.ip_address,
                      "name": ip.direction,
                      }
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def staff_profile(request):
    user = Users.objects.get(id=request.user.id)
    staff = Instructor.objects.get(admin=user)
    context = {
        "user": user,
        "staff": staff
    }
    return render(request, 'instructor_templates/staff_profile.html', context)


def staff_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('staff_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')
        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        try:
            customuser = Users.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Instructor.objects.get(admin=customuser.id)
            staff.address = address
            staff.profile_pic = profile_pic_url
            staff.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('staff_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('staff_profile')
