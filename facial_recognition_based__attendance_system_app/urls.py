from django.urls import path, include
from . import views
from . import ICT_ProfessionalViews, DepartmentHeadViews, InstructorViews, StudentViews
from .DepartmentHeadViews import edit_assign_instructor, edit_assign_instructor_save


urlpatterns = [
    path('', views.main_home, name="main_home"),
    path('login/', views.loginPage, name="login"),
    path('contact/', views.contact, name="contact"),
    path('password_reset/', views.password_reset, name="password_reset"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),

    # URLS for Admin
    path('admin_home/', ICT_ProfessionalViews.admin_home, name="admin_home"),

    path('add_head/', ICT_ProfessionalViews.add_head, name="add_head"),
    path('add_head_save/', ICT_ProfessionalViews.add_head_save, name="add_head_save"),
    path('manage_head/', ICT_ProfessionalViews.manage_head, name="manage_head"),
    path('edit_head/<head_id>/', ICT_ProfessionalViews.edit_head, name="edit_head"),
    path('edit_head_save/', ICT_ProfessionalViews.edit_head_save, name="edit_head_save"),
    path('delete_head/<head_id>/', ICT_ProfessionalViews.delete_head, name="delete_head"),

    path('add_staff/', ICT_ProfessionalViews.add_staff, name="add_staff"),
    path('add_staff_save/', ICT_ProfessionalViews.add_staff_save, name="add_staff_save"),
    path('manage_staff/', ICT_ProfessionalViews.manage_staff, name="manage_staff"),
    path('edit_staff/<staff_id>/', ICT_ProfessionalViews.edit_staff, name="edit_staff"),
    path('edit_staff_save/', ICT_ProfessionalViews.edit_staff_save, name="edit_staff_save"),
    path('delete_staff/<staff_id>/', ICT_ProfessionalViews.delete_staff, name="delete_staff"),

    path('add_college/', ICT_ProfessionalViews.add_college, name="add_college"),
    path('add_college_save/', ICT_ProfessionalViews.add_college_save, name="add_college_save"),
    path('manage_college/', ICT_ProfessionalViews.manage_college, name="manage_college"),
    path('edit_college/<college_id>/', ICT_ProfessionalViews.edit_college, name="edit_college"),
    path('edit_college_save/', ICT_ProfessionalViews.edit_college_save, name="edit_college_save"),
    path('delete_college/<college_id>/', ICT_ProfessionalViews.delete_college, name="delete_college"),

    path('manage_session/', ICT_ProfessionalViews.manage_session, name="manage_session"),
    path('add_session/', ICT_ProfessionalViews.add_session, name="add_session"),
    path('add_session_save/', ICT_ProfessionalViews.add_session_save, name="add_session_save"),
    path('edit_session/<session_id>', ICT_ProfessionalViews.edit_session, name="edit_session"),
    path('edit_session_save/', ICT_ProfessionalViews.edit_session_save, name="edit_session_save"),
    path('delete_session/<session_id>/', ICT_ProfessionalViews.delete_session, name="delete_session"),

    path('add_student/', ICT_ProfessionalViews.add_student, name="add_student"),
    path('add_student_save/', ICT_ProfessionalViews.add_student_save, name="add_student_save"),
    path('edit_student/<student_id>', ICT_ProfessionalViews.edit_student, name="edit_student"),
    path('edit_student_save/', ICT_ProfessionalViews.edit_student_save, name="edit_student_save"),
    path('manage_student/', ICT_ProfessionalViews.manage_student, name="manage_student"),
    path('delete_student/<student_id>/', ICT_ProfessionalViews.delete_student, name="delete_student"),

    path('add_department/', ICT_ProfessionalViews.add_department, name="add_department"),
    path('add_department_save/', ICT_ProfessionalViews.add_department_save, name="add_department_save"),
    path('manage_department/', ICT_ProfessionalViews.manage_department, name="manage_department"),
    path('edit_department/<department_id>/', ICT_ProfessionalViews.edit_department, name="edit_department"),
    path('edit_department_save/', ICT_ProfessionalViews.edit_department_save, name="edit_department_save"),
    path('delete_department/<department_id>/', ICT_ProfessionalViews.delete_department, name="delete_department"),

    path('check_email_exist/', ICT_ProfessionalViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', ICT_ProfessionalViews.check_username_exist, name="check_username_exist"),

    path('student_feedback_message/', ICT_ProfessionalViews.student_feedback_message, name="student_feedback_message"),
    path('student_feedback_message_reply/', ICT_ProfessionalViews.student_feedback_message_reply,
         name="student_feedback_message_reply"),

    path('everyone_feedback_message/', ICT_ProfessionalViews.everyone_feedback_message, name="everyone_feedback_message"),
    path('delete_everyone_feedback/<contact_id>/', ICT_ProfessionalViews.delete_everyone_feedback, name="delete_everyone_feedback"),
    path('staff_feedback_message/', ICT_ProfessionalViews.staff_feedback_message, name="staff_feedback_message"),
    path('staff_feedback_message_reply/', ICT_ProfessionalViews.staff_feedback_message_reply, name="staff_feedback_message_reply"),

    path('admin_view_attendance/', ICT_ProfessionalViews.admin_view_attendance, name="admin_view_attendance"),
    path('admin_view_final_attendance/', ICT_ProfessionalViews.admin_view_final_attendance, name="admin_view_final_attendance"),
    path('load_batches/', ICT_ProfessionalViews.load_batches, name="load_batches"),
    path('load_batches_final/', ICT_ProfessionalViews.load_batches_final, name="load_batches_final"),
    path('load_sections/', ICT_ProfessionalViews.load_sections, name="load_sections"),
    path('load_sections_final/', ICT_ProfessionalViews.load_sections_final, name="load_sections_final"),
    path('load_subjects/', ICT_ProfessionalViews.load_subjects, name="load_subjects"),
    path('load_attendance_department/', ICT_ProfessionalViews.load_attendance_department, name="load_attendance_department"),
    path('load_attendance_batch/', ICT_ProfessionalViews.load_attendance_batch, name="load_attendance_batch"),
    path('load_attendance_section/', ICT_ProfessionalViews.load_attendance_section, name="load_attendance_section"),
    path('admin_get_attendance_student/', ICT_ProfessionalViews.admin_get_attendance_student, name="admin_get_attendance_student"),
    path('admin_get_attendance_student_batch/', ICT_ProfessionalViews.admin_get_attendance_student_batch, name="admin_get_attendance_student_batch"),
    path('admin_get_attendance_student_section/', ICT_ProfessionalViews.admin_get_attendance_student_section, name="admin_get_attendance_student_section"),
    path('admin_view_final_taking_list/', ICT_ProfessionalViews.admin_view_final_taking_list, name="admin_view_final_taking_list"),

    path('admin_profile/', ICT_ProfessionalViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', ICT_ProfessionalViews.admin_profile_update, name="admin_profile_update"),

    # URLS For Facial Recognition, Admin
    path('predict_image/', ICT_ProfessionalViews.test_image, name='predict_image'),
    path('perform_predicting_image/', ICT_ProfessionalViews.perform_test_image, name='perform_predicting_image'),

    path('train_model/', ICT_ProfessionalViews.train_model, name='train_model'),
    path('perform_train_model/', ICT_ProfessionalViews.perform_train_model, name='perform_train_model'),
    path('manage_train_model/', ICT_ProfessionalViews.manage_train_model, name='manage_train_model'),
    path('edit_training_parameters/<model_id>', ICT_ProfessionalViews.edit_training_parameters, name='edit_training_parameters'),
    path('edit_training_parameters_save/', ICT_ProfessionalViews.edit_training_parameters_save,
         name='edit_training_parameters_save'),
    path('delete_training_parameters/<model_id>/', ICT_ProfessionalViews.delete_training_parameters,
         name='delete_training_parameters'),

    path('upload_dataset/', ICT_ProfessionalViews.upload_dataset, name='upload_dataset'),
    path('upload_dataset_save/', ICT_ProfessionalViews.upload_dataset_save, name='upload_dataset_save'),
    path('manage_uploaded_dataset/', ICT_ProfessionalViews.manage_uploaded_dataset, name='manage_uploaded_dataset'),
    path('delete_uploaded_dataset/<dataset_id>/', ICT_ProfessionalViews.delete_uploaded_dataset, name='delete_uploaded_dataset'),

    # URLS for Head
    path('head_home/', DepartmentHeadViews.head_home, name="head_home"),

    path('head/add_batch/', DepartmentHeadViews.add_batch, name="head_add_batch"),
    path('head/add_batch_save/', DepartmentHeadViews.add_batch_save, name="head_add_batch_save"),
    path('head/manage_batch/', DepartmentHeadViews.manage_batch, name="head_manage_batch"),
    path('head/edit_batch/<batch_id>/', DepartmentHeadViews.edit_batch, name="head_edit_batch"),
    path('head/edit_batch_save/', DepartmentHeadViews.edit_batch_save, name="head_edit_batch_save"),
    path('head/delete_batch/<batch_id>/', DepartmentHeadViews.delete_batch, name="head_delete_batch"),

    path('head/manage_attendance_weight/', DepartmentHeadViews.manage_attendance_weight, name="head_manage_session"),
    path('head/add_attendance_weight/', DepartmentHeadViews.add_attendance_weight, name="head_add_session"),
    path('head/add_attendance_weight_save/', DepartmentHeadViews.add_attendance_weight_save, name="head_add_session_save"),
    path('head/edit_attendance_weight/<weight_id>', DepartmentHeadViews.edit_attendance_weight, name="head_edit_session"),
    path('head/edit_attendance_weight_save/', DepartmentHeadViews.edit_attendance_weight_save, name="head_edit_session_save"),
    path('head/delete_attendance_weight/<weight_id>/', DepartmentHeadViews.delete_attendance_weight, name="head_delete_session"),


    path('head/register_for_course/', DepartmentHeadViews.register_for_course, name="register_for_course"),
    path('head/head_get_students/', DepartmentHeadViews.head_get_students, name="head_get_students"),
    path('head/register_for_course_save/', DepartmentHeadViews.register_for_course_save, name="register_for_course_save"),
    path('head/edit_register_for_course/<register_id>', DepartmentHeadViews.edit_register_for_course,
         name="edit_register_for_course"),
    path('head/edit_register_for_course_save/', DepartmentHeadViews.edit_register_for_course_save,
         name="edit_register_for_course_save"),
    path('head/manage_register_for_course/', DepartmentHeadViews.manage_register_for_course, name="manage_register_for_course"),
    path('head/delete_register_for_course/<register_id>/', DepartmentHeadViews.delete_register_for_course,
         name="delete_register_for_course"),

    path('head/add_subject/', DepartmentHeadViews.add_subject, name="head_add_subject"),
    path('head/add_subject_save/', DepartmentHeadViews.add_subject_save, name="head_add_subject_save"),
    path('head/manage_subject/', DepartmentHeadViews.manage_subject, name="head_manage_subject"),
    path('head/edit_subject/<subject_id>/', DepartmentHeadViews.edit_subject, name="head_edit_subject"),
    path('head/edit_subject_save/', DepartmentHeadViews.edit_subject_save, name="head_edit_subject_save"),
    path('head/delete_subject/<subject_id>/', DepartmentHeadViews.delete_subject, name="head_delete_subject"),
    path('head/add_subject/', DepartmentHeadViews.add_subject, name="head_add_subject"),

    path('head/assign_instructor/', DepartmentHeadViews.assign_instructor, name="assign_instructor"),
    path('head/assign_instructor_save/', DepartmentHeadViews.assign_instructor_save, name="assign_instructor_save"),
    path('head/manage_assign_instructor/', DepartmentHeadViews.manage_assign_instructor, name="manage_assign_instructor"),



    path('head/edit_assign_instructor/<int:assign_id>', DepartmentHeadViews.edit_assign_instructor, name='edit_assign_instructor'),


    
    path('head/edit_assign_instructor_save/', DepartmentHeadViews.edit_assign_instructor_save,
         name="edit_assign_instructor_save"),
    path('head/delete_assign_instructor/<assign_instructor_id>/', DepartmentHeadViews.delete_assign_instructor,
         name="delete_assign_instructor"),
#     path('head/check_email_exist/', DepartmentHeadViews.check_email_exist, name="head_check_email_exist"),
    path('head/check_username_exist/', DepartmentHeadViews.check_username_exist, name="head_check_username_exist"),

    path('head/student_feedback_message/', DepartmentHeadViews.student_feedback_message, name="head_student_feedback_message"),
    path('head/student_feedback_message_reply/', DepartmentHeadViews.student_feedback_message_reply,
         name="head_student_feedback_message_reply"),

    path('head/staff_feedback_message/', DepartmentHeadViews.staff_feedback_message, name="head_staff_feedback_message"),
    path('head/staff_feedback_message_reply/', DepartmentHeadViews.staff_feedback_message_reply,
         name="head_staff_feedback_message_reply"),

    path('head/staff_leave_view/', DepartmentHeadViews.staff_leave_view, name="head_staff_leave_view"),
    path('head/staff_leave_approve/<leave_id>/', DepartmentHeadViews.staff_leave_approve, name="head_staff_leave_approve"),
    path('head/staff_leave_reject/<leave_id>/', DepartmentHeadViews.staff_leave_reject, name="head_staff_leave_reject"),

    path('head/set_student_status/', DepartmentHeadViews.set_student_status, name="set_student_status"),
    path('head/student_status_save/', DepartmentHeadViews.student_status_save, name="student_status_save"),
    path('head/manage_student_status/', DepartmentHeadViews.manage_student_status, name="manage_student_status"),
    path('head/delete_student_status/<status_id>/', DepartmentHeadViews.delete_student_status, name="delete_student_status"),

    path('head/head_view_attendance/', DepartmentHeadViews.head_view_attendance, name="head_view_attendance"),
    path('head/head_manage_attendance/', DepartmentHeadViews.head_manage_attendance, name="head_manage_attendance"),
    path('head/head_view_attendance_final/', DepartmentHeadViews.head_view_attendance_final, name="head_view_attendance_final"),
    path('head/head_get_attendance_dates/', DepartmentHeadViews.head_get_attendance_dates, name="head_get_attendance_dates"),
    path('head/head_get_attendance_student/', DepartmentHeadViews.head_get_attendance_student,
         name="head_get_attendance_student"),
    path('head_delete_attendance/<attendance_id>/', DepartmentHeadViews.head_delete_attendance, name="head_delete_attendance"),

    path('head/head_profile/', DepartmentHeadViews.head_profile, name="head_profile"),
    path('head/head_profile_pic/', DepartmentHeadViews.head_profile_pic, name="head_profile_pic"),
    path('head/head_profile_update/', DepartmentHeadViews.head_profile_update, name="head_profile_update"),

    # URLS for Staff
    path('staff_home/', InstructorViews.staff_home, name="staff_home"),
    path('staff_take_attendance/', InstructorViews.staff_take_attendance, name="staff_take_attendance"),
    path('fr_take_attendance/', InstructorViews.fr_take_attendance, name="fr_take_attendance"),
    path('staff_fr_view_attendanceFR/', InstructorViews.staff_fr_view_attendanceFR, name="staff_fr_view_attendanceFR"),
    path('fr_take_attendance_save/', InstructorViews.fr_take_attendance_save, name="fr_take_attendance_save"),
    path('get_students/', InstructorViews.get_students, name="get_students"),
    path('save_attendance_data/', InstructorViews.save_attendance_data, name="save_attendance_data"),
    path('staff_update_attendance/', InstructorViews.staff_update_attendance, name="staff_update_attendance"),
    path('get_attendance_dates/', InstructorViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student/', InstructorViews.get_attendance_student, name="get_attendance_student"),
    path('update_attendance_data/', InstructorViews.update_attendance_data, name="update_attendance_data"),
    path('staff_fr_view_attendance/', InstructorViews.staff_fr_view_attendance, name="staff_fr_view_attendance"),
    path('staff_view_attendance_final/', InstructorViews.staff_view_attendance_final, name="staff_view_attendance_final"),
    path('delete_attendance/<attendance_id>/', InstructorViews.delete_attendance, name="delete_attendance"),
    path('delete_attendancefr/<attendance_id>/', InstructorViews.delete_attendancefr, name="delete_attendancefr"),

    path('staff_apply_leave/', InstructorViews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save/', InstructorViews.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback/', InstructorViews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save/', InstructorViews.staff_feedback_save, name="staff_feedback_save"),

    path('staff_student_leave_view/', InstructorViews.student_leave_view, name="staff_student_leave_view"),
    path('staff_student_leave_approve/<leave_id>/', InstructorViews.student_leave_approve,
         name="staff_student_leave_approve"),
    path('staff_student_leave_reject/<leave_id>/', InstructorViews.student_leave_reject, name="staff_student_leave_reject"),

    path('staff_student_feedback_message/', InstructorViews.student_feedback_message, name="staff_student_feedback_message"),
    path('staff_student_feedback_message_reply/', InstructorViews.student_feedback_message_reply,
         name="staff_student_feedback_message_reply"),

    path('staff_profile/', InstructorViews.staff_profile, name="staff_profile"),
    path('staff_profile_update/', InstructorViews.staff_profile_update, name="staff_profile_update"),

    path('staff_add_camera/', InstructorViews.add_camera, name="add_camera"),
    path('staff_add_camera_save/', InstructorViews.add_camera_save, name="add_camera_save"),
    path('staff_manage_camera/', InstructorViews.manage_camera, name="manage_camera"),
    path('staff_edit_camera/<camera_id>/', InstructorViews.edit_camera, name="edit_camera"),
    path('staff_edit_camera_save/', InstructorViews.edit_camera_save, name="edit_camera_save"),
    path('staff_delete_camera/<camera_id>/', InstructorViews.delete_camera, name="delete_camera"),

    # URLS for Student
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('student_view_attendance/', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post/', StudentViews.student_view_attendance_post,
         name="student_view_attendance_post"),
    path('student_apply_leave/', StudentViews.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save/', StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback/', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save/', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"),
    path('student_base/', StudentViews.student_base, name="student_base"),

    # dependent dropdown lists related with ajax
    path('load_departments/', ICT_ProfessionalViews.load_departments, name='load_departments'),
    path('load_staffs/', ICT_ProfessionalViews.load_staffs, name='load_staffs'),
    path('head_load_subjects/', DepartmentHeadViews.load_subjects, name='head_load_subjects'),
    path('load_subjects_batch/', DepartmentHeadViews.load_subjects_batch, name='load_subjects_batch'),
    path('head_get_student_final/', DepartmentHeadViews.head_get_student_final, name='head_get_student_final'),
    path('staff_get_student_final/', InstructorViews.staff_get_student_final, name='staff_get_student_final'),
    path('load_sections_batch/', DepartmentHeadViews.load_sections_batch, name='load_sections_batch'),
    path('load_ip_address/', InstructorViews.load_ip_address, name='load_ip_address'),
    path('load_subjects_section_batch/', DepartmentHeadViews.load_subjects_section_batch, name='load_subjects_section_batch'),





]
